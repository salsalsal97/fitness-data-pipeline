### IMPORTS ###
import gspread
import os
import json
from google.oauth2.service_account import Credentials
from core.paths import GOOGLE_CREDENTIALS_FILE
from core.config import GOOGLE_SCOPES

### MAIN ###
def get_google_credentials():
    """
    Connects to GCP
    """
    credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    if credentials_json:
        info = json.loads(credentials_json)
        return Credentials.from_service_account_info(
            info,
            scopes=GOOGLE_SCOPES
        )
    return Credentials.from_service_account_file(
        str(GOOGLE_CREDENTIALS_FILE),
        scopes=GOOGLE_SCOPES
    )

def get_gspread_client():
    """
    Builds connection
    """
    creds = get_google_credentials()
    return gspread.authorize(creds)

def get_worksheet(spreadsheet_name: str, worksheet_name: str):
    """
    Connects to and opens sheets
    """
    gc = get_gspread_client()
    spreadsheet = gc.open(spreadsheet_name)
    return spreadsheet.worksheet(worksheet_name)

def date_exists(sheet, target_date):
    dates = sheet.col_values(1)[1:]
    return target_date.isoformat() in dates

def find_rows_by_date(sheet, target_date):
    dates = sheet.col_values(1)
    target = target_date.isoformat()
    matching_rows = []
    for row_number, value in enumerate(dates, start=1):
        if value == target:
            matching_rows.append(row_number)
    return matching_rows

def delete_rows(sheet, row_numbers):
    for row_number in reversed(row_numbers):
        sheet.delete_rows(row_number)