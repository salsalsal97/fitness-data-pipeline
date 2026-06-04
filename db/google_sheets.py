### IMPORTS ###
from core.paths import GOOGLE_CREDENTIALS_FILE
from core.config import GOOGLE_SCOPES
from google.oauth2.service_account import Credentials
import gspread

### MAIN ###
def get_gspread_client():
    """
    Connects to GCP
    """
    creds = Credentials.from_service_account_file(
        str(GOOGLE_CREDENTIALS_FILE),
        scopes=GOOGLE_SCOPES
    )
    return gspread.authorize(creds)

def get_worksheet(spreadsheet_name: str, worksheet_name: str):
    """
    Connects to and opens sheets
    """
    gc = get_gspread_client()
    spreadsheet = gc.open(spreadsheet_name)
    return spreadsheet.worksheet(worksheet_name)