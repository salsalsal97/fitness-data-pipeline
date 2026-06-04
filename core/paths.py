from pathlib import Path
BASE_DIR = Path(__file__).resolve()
PROJECT_ROOT = BASE_DIR.parents[1]
SECRETS_DIR = PROJECT_ROOT / "secrets"
COOKIES_FILE = SECRETS_DIR / "cookies.txt"
GOOGLE_CREDENTIALS_FILE = SECRETS_DIR / "credentials.json"
