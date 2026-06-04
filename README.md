# Fitness Automation Pipeline

Personal ETL project that extracts nutrition, body metrics, and workout data from MyFitnessPal, transforms it into structured records, and loads it into Google Sheets for dashboarding.

## Features

- Scrapes daily calories and macros from MyFitnessPal
- Parses structured note metrics such as steps, weight, and waist
- Parses exercise diary entries
- Maps raw MFP exercise names to canonical dashboard names
- Writes daily metrics and progress records to Google Sheets
- Uses schema validation before loading

## Tech Stack

- Python
- BeautifulSoup
- requests
- gspread
- Google Sheets API

## Notes

This project uses a local `secrets/` folder for private credentials and cookies. These files are intentionally excluded from version control.