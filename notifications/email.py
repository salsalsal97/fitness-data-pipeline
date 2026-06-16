import os
import resend
from core.config import EMAIL
from pathlib import Path

def send_status_email(subject, body):
    key_file = Path("secrets/resend_api_key.txt")
    api_key = os.getenv("RESEND_API_KEY")
    if api_key is None:
        with open(key_file) as f:
            api_key = f.read().strip()
    resend.api_key = api_key
    resend.Emails.send({
        "from": EMAIL["from"],
        "to": EMAIL["to"],
        "subject": subject,
        "text": body,
    })

def format_success(summary):
    record = summary["daily_record"]
    steps_status = (
        record["steps"]
        if record["steps"] is not None
        else "MISSING - please update MFP note"
    )
    warnings = []
    if record["steps"] is None:
        warnings.append("Steps are missing")
    warning_text = (
        "\nWarnings:\n- " + "\n- ".join(warnings)
        if warnings
        else ""
    )
    return f"""
Fitness pipeline succeeded.

Date: {summary["date"]}

Nutrition:
Calories: {record["calories"]}
Protein: {record["protein"]}g
Carbs: {record["carbohydrates"]}g
Fat: {record["fat"]}g
Steps: {steps_status}
Weight: {record["weight"]}
Waist: {record["waist"]}
Gym: {record["gym"]}

Progress records updated: {summary["progress_count"]}

{warning_text}
""".strip()

def format_failure(target_date, error):
    return f"""
Fitness pipeline failed.

Date: {target_date}

Error:
{error}
""".strip()