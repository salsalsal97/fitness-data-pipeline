# Fitness Data Pipeline

A personal ETL (Extract, Transform, Load) project that automates the collection, transformation, and storage of nutrition, body metrics, and workout data from MyFitnessPal into Google Sheets for analysis and dashboarding.

## Overview

This project was built to automate the manual tracking of fitness and nutrition data. The pipeline extracts information from MyFitnessPal, transforms it into a structured format, validates the resulting records, and loads them into Google Sheets where the data can be visualised and analysed.

The project follows a modular ETL architecture with separate layers for extraction, transformation, validation, and persistence.

## Features

### Nutrition Tracking

* Extracts daily calorie intake from MyFitnessPal
* Extracts daily macronutrients:

  * Protein
  * Carbohydrates
  * Fat
* Stores one consolidated nutrition record per day

### Body Metrics

Extracts custom metrics recorded in MyFitnessPal notes, including:

* Steps
* Weight
* Waist circumference

Metrics are optional and the pipeline gracefully handles missing values.

### Workout Tracking

* Extracts strength training exercises from MyFitnessPal
* Maps MyFitnessPal exercise names to canonical exercise names used in downstream reporting
* Groups sets and reps into a structured format
* Categorises exercises into workout types:

  * Push
  * Pull
  * Legs
  * Core
  * Cardio

### Data Validation

* Schema validation before loading
* Missing value handling
* Exercise mapping validation
* Duplicate prevention and safe reruns

### Google Sheets Integration

Writes data to two worksheets:

#### Nutrition

One row per day containing:

* Date
* Day
* Calories
* Protein
* Carbohydrates
* Fat
* Gym Flag
* Steps
* Weight
* Waist

#### Progress

One row per exercise containing:

* Date
* Exercise Type
* Exercise Name
* Set / Rep Details
* Notes

## Project Structure

```text
Fitness/
│
├── core/
│   ├── config.py
│   ├── paths.py
│   └── pipeline.py
│
├── ingestion/
│   └── myfitnesspal.py
│
├── processing/
│   └── records.py
│
├── db/
│   └── google_sheets.py
│
├── secrets/
│   └── (excluded from version control)
│
├── tests/
│
├── requirements_windows.txt
├── .gitignore
└── README.md
```

## Technology Stack

* Python
* Requests
* BeautifulSoup4
* Google Sheets API
* gspread
* OAuth2 Service Accounts

## Running the Pipeline

Activate the virtual environment:

```bash
.\venv_windows\Scripts\activate
```

Run the daily pipeline:

```bash
python scripts/run_mfp_daily.py
```

The pipeline processes the previous day's data and updates the configured Google Sheets workbook.

## Configuration

Configuration is managed through:

```text
core/config.py
```

including:

* MyFitnessPal username
* Google Sheets worksheet names
* Data schemas
* Pipeline settings

## Security

The following files are intentionally excluded from version control:

* cookies.txt
* credentials.json
* service account credentials
* any files stored within the `secrets/` directory

## Current Limitations

* Relies on MyFitnessPal web scraping rather than an official API
* Requires valid MyFitnessPal authentication cookies
* Custom metrics (steps, weight, waist) are currently supplied through structured diary notes
* Exercise mappings must be maintained manually for new exercise types

## Future Improvements

Potential future enhancements include:

* Automated scheduling
* Unit tests
* Structured logging
* Database backend
* Dashboard automation
* Cloud deployment
* Additional fitness data sources (Fitbit, Garmin, etc.)

## Author

Salman Fawad

Built as a personal data engineering and automation project to support long-term fitness tracking and analytics.
