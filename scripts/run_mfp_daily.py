############################################# MYFITNESSPAL AUTOMATION #############################################
# FIRST ACTIVATE ENVIRONMENT WITH PACKAGES AS IN requirements.txt
# SOMETIMES MAY NEED TO REGENERATE '.\secrets\cookies.txt' (IF AUTHENTICATION ERROR)
###################################################################################################################

### IMPORTS ###
from datetime import date, timedelta
from core.pipeline import run_daily_pipeline
target_date = date.today() - timedelta(days=1)

### MAIN ###
def main():
    run_daily_pipeline(target_date)

if __name__ == "__main__":
    main()

### TO RUN FOR A RANGE OF DATES ###
#import pandas as pd
#dates = pd.date_range(start='2026-04-22',end='2026-06-03')
#for dt in dates:
#   run_daily_pipeline(dt.date())
