############################################# MYFITNESSPAL AUTOMATION #############################################
# FIRST ACTIVATE venv_windows ENVIRONMENT IN 'C:\Users\salma\Desktop\Fitness' (.\venv_windows\Scripts\activate)
# SOMETIMES MAY NEED TO REGENERATE 'C:\Users\salma\Desktop\Fitness\secrets\cookies.txt' (IF AUTHENTICATION ERROR)
###################################################################################################################

### IMPORTS ###
from datetime import date, timedelta
from core.pipeline import run_daily_pipeline
target_date = date.today() - timedelta(days=2)
#target_date = date.today() - timedelta(days=1)
#target_date = date(2026,5,10)

### MAIN ###
def main():
    run_daily_pipeline(target_date)

if __name__ == "__main__":
    main()

### TO RUN FOR A RANGE ###
#import pandas as pd
#dates = pd.date_range(start='2026-04-22',end='2026-06-03')
#for dt in dates:
#   run_daily_pipeline(dt.date())
