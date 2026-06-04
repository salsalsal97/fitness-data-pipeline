### IMPORTS ###
import requests
import http.cookiejar as cj
import re
import csv
from bs4 import BeautifulSoup
from core.paths import COOKIES_FILE
from processing.records import build_base_record
from collections import defaultdict
from pathlib import Path

### MAIN ###
def parse_numeric_value(text):
    """
    Helper function to get actual values for Calories / Macros
    """
    text = text.split('%')[0]
    numbers = re.findall(r"\d+", text.replace(",", ""))
    return int(numbers[0]) if numbers else None

def load_session():
    """
    Load MFP session
    """
    jar = cj.MozillaCookieJar(str(COOKIES_FILE))
    jar.load(ignore_discard=True, ignore_expires=True)
    session = requests.Session()
    for cookie in jar:
        session.cookies.set(cookie.name, cookie.value)
    session.headers.update({ "User-Agent": "Mozilla/5.0", "Accept-Language": "en-GB,en;q=0.9" })
    return session

def extract_mfp_page(target_date, username, diary_type):
    """
    Extracts daily nutrition totals from MFP
    """
    session = load_session()
    url = f"https://www.myfitnesspal.com/{diary_type}/diary/{username}?date={str(target_date)}"
    response = session.get(url)
    if response.status_code != 200:
        raise RuntimeError("MFP request failed - cookies likely expired")
    print("Status:", response.status_code) # Should return 200
    return response.text

def parse_mfp_totals(html):
    """
    Transforms daily nutrition totals from MFP
    """
    soup = BeautifulSoup(html, "html.parser")
    totals_row = None
    for tr in soup.find_all("tr"):
        if "total" in tr.get_text().lower():
            totals_row = tr
            break
    if not totals_row:
        raise ValueError("Totals row not found - MFP structure may have changed")
    values = [td.get_text(" ", strip=True) for td in totals_row.find_all("td")]
    totals = {
        "calories": parse_numeric_value(values[1]),
        "protein": parse_numeric_value(values[4]),
        "carbohydrates": parse_numeric_value(values[2]),
        "fat": parse_numeric_value(values[3])
    }
    if any(v is None for v in totals.values()):
        raise ValueError(f"Incomplete totals extracted: {totals}")
    return totals

def parse_note_metrics(html):
    """
    Function to get steps, weight, waist
    """
    soup = BeautifulSoup(html, "html.parser")
    note = None
    for p in soup.find_all("p"):
        if "#steps=" in p.get_text().lower():
            note = p
            break
    if not note:
        return {
            "steps": None,
            "weight": None,
            "waist": None
        }
        #raise ValueError("Note not found - MFP structure may have changed")
    text = note.get_text("\n", strip=True)
    match_steps = re.search(rf"steps=([\d\.]+)", text)
    match_weight = re.search(rf"weight=([\d\.]+)", text)
    match_waist = re.search(rf"waist=([\d\.]+)", text)
    #if not match_steps:
    #    raise ValueError("Steps not found in note")
    #else:
    steps = int(match_steps.group(1))
    if not match_weight:
        weight = None
    else:
        weight = float(match_weight.group(1))
    if not match_waist:
        waist = None
    else:
        waist = float(match_waist.group(1))
    output = {
        "steps": steps,
        "weight": weight,
        "waist": waist
    }
    return output

def parse_exercises(html):
    """
    Function to get exercises
    """
    outs = []
    soup = BeautifulSoup(html, "html.parser")
    exercise_table = None
    for table in soup.find_all("table"):
        if "strength training" in table.get_text().lower():
            exercise_table = table
            break
    if not exercise_table:
        return []
    table_rows = exercise_table.find_all("tr")
    for row in table_rows:
        cells = row.find_all("td")
        values = [cell.get_text(" ",strip=True) for cell in cells]
        if len(values) != 4:
            continue
        exercise, sets, reps, weight = values
        if not exercise or not sets or not reps or not weight:
            continue
        if not sets.isdigit() or not reps.isdigit():
            continue
        outs.append(values)
    return outs

def load_exercise_mappings():
    """
    Loads MFP exercise map and carries out mapping
    """
    mappings = {}
    mapping_file = Path("core/exercise_mappings.csv")
    with open(mapping_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mappings[row["MFP_Exercise"]] = {
                "exercise": row["Exercise"],
                "type": row["Type"]
            }
    return mappings

def transform_exercises(raw_rows, target_date):
    """
    Transform exericses to correct format
    """
    if not raw_rows:
        return []
    mappings = load_exercise_mappings()
    grouped = defaultdict(list)
    exercise_types = {}
    for row in raw_rows:
        mfp_name = row[0]
        sets = int(row[1])
        reps = int(row[2])
        weight_lbs = float(row[3])
        weight_kg = round(weight_lbs * 0.453592)
        if mfp_name not in mappings:
            print(f"WARNING: No mapping found for {mfp_name}")
            continue
        exercise_name = mappings[mfp_name]["exercise"]
        exercise_type = mappings[mfp_name]["type"]
        exercise_types[exercise_name] = exercise_type
        set_string = f"{reps}×{weight_kg}kg"
        for _ in range(sets):
            grouped[exercise_name].append(set_string)
    records = []
    for exercise_name, sets_list in grouped.items():
        records.append({
            "date": target_date.isoformat(),
            "type": exercise_types[exercise_name],
            "exercise": exercise_name,
            "details": ", ".join(sets_list),
            "notes": ""
        })
    return records

def build_mfp_record(target_date, nutrition_data, body_metrics, gym):
    """
    Builds row to append to dataset
    """
    record = build_base_record(target_date)
    record.update({
        "calories": nutrition_data["calories"],
        "protein": nutrition_data["protein"],
        "carbohydrates": nutrition_data["carbohydrates"],
        "fat": nutrition_data["fat"],
        "gym": gym,
        "steps": body_metrics["steps"],
        "weight": body_metrics["weight"],
        "waist": body_metrics["waist"]
    })
    return record

def record_to_row(record, schema):
    """
    Get value for each column in the schema
    """
    return [
        record[col] if record[col] is not None else ""
        for col in schema
    ]
