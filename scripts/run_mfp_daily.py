############################################# MYFITNESSPAL AUTOMATION #############################################
# FIRST ACTIVATE ENVIRONMENT WITH PACKAGES AS IN requirements.txt
# SOMETIMES MAY NEED TO REGENERATE '.\secrets\cookies.txt' (IF AUTHENTICATION ERROR)
###################################################################################################################

### IMPORTS ###
from datetime import date, timedelta
from core.pipeline import run_daily_pipeline
from notifications.email import send_status_email, format_success, format_failure
target_date = date.today() - timedelta(days=1)

### MAIN ###
def main():
    try:
        summary = run_daily_pipeline(target_date)
        send_status_email(
            subject=(
                f"Fitness pipeline succeeded with warning - {target_date}"
                if summary["daily_record"]["steps"] is None
                else f"Fitness pipeline succeeded - {target_date}"
            ),
            body=format_success(summary),
        )
    except Exception as e:
        send_status_email(
            subject=f"Fitness pipeline failed - {target_date}",
            body=format_failure(target_date,e),
        )
        raise

if __name__ == "__main__":
    main()

### TO RUN FOR A RANGE OF DATES ###
#import pandas as pd
#dates = pd.date_range(start='2026-04-22',end='2026-06-03')
#for dt in dates:
#   run_daily_pipeline(dt.date())
