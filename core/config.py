WRITE_TO_SHEETS = True

GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

GOOGLE_SPREADSHEET = "MFP_Daily_Log"

WORKSHEETS = {
    "nutrition": "Nutrition",
    "progress": "Progress"
}

MFP = {
    "username": "salsalsal97"
}

MFP_SCHEMA = [
    "date",
    "day",
    "calories",
    "protein",
    "carbohydrates",
    "fat",
    "gym",
    "steps",
    "weight",
    "waist",
]

PROGRESS_SCHEMA = [
    "date",
    "type",
    "exercise",
    "details",
    "notes"
]

EMAIL = {
    "from": "Fitness Pipeline <onboarding@resend.dev>",
    "to": "salman.fawad@hotmail.com"
}
