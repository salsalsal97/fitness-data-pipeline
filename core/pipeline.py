### IMPORTS ###
from ingestion.myfitnesspal import extract_mfp_page, build_mfp_record, parse_mfp_totals, parse_note_metrics, parse_exercises, transform_exercises, record_to_row #get_mfp_totals
from db.google_sheets import get_worksheet
from core.config import MFP, GOOGLE_SPREADSHEET, WORKSHEETS, MFP_SCHEMA, PROGRESS_SCHEMA, WRITE_TO_SHEETS

### MAIN ###
def validate_record(record, schema):
    if set(record.keys()) != set(schema):
        raise ValueError(f"Schema mismatch: {record.keys()} vs {schema}")

def build_daily_record(target_date, food_html, exercise_html, gym):
    nutrition_data = parse_mfp_totals(food_html)
    body_metrics = parse_note_metrics(exercise_html)
    record = build_mfp_record(target_date, nutrition_data, body_metrics, gym)
    return record

def run_progress_pipeline(target_date, exercise_html):
    raw_rows = parse_exercises(exercise_html)
    records = transform_exercises(raw_rows, target_date)
    return records

def run_daily_data_pipeline(target_date):
    food_html = extract_mfp_page(target_date, MFP["username"], "food")
    exercise_html = extract_mfp_page(target_date, MFP["username"], "exercise")
    progress_records = run_progress_pipeline(target_date, exercise_html)
    gym = 1 if len(progress_records) > 0 else 0
    mfp_record = build_daily_record(target_date, food_html, exercise_html, gym)
    return mfp_record, progress_records

def run_daily_pipeline(target_date):
    daily_record, progress_records = run_daily_data_pipeline(target_date)
    validate_record(daily_record, MFP_SCHEMA)
    nutrition_sheet = get_worksheet(
        GOOGLE_SPREADSHEET,
        WORKSHEETS["nutrition"]
    )
    if WRITE_TO_SHEETS:
        nutrition_sheet.append_row(record_to_row(daily_record, MFP_SCHEMA))
    print(f"Processed {target_date}: {daily_record}")
    progress_sheet = get_worksheet(
        GOOGLE_SPREADSHEET,
        WORKSHEETS["progress"]
    )
    for record in progress_records:
        validate_record(record, PROGRESS_SCHEMA)
        if WRITE_TO_SHEETS:
            progress_sheet.append_row(record_to_row(record, PROGRESS_SCHEMA))
    print(f"Processed {len(progress_records)} progress records: {progress_records}")
