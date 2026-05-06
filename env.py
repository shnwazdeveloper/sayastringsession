import os

from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("API_ID", "").strip()
API_HASH = os.getenv("API_HASH", "").strip()
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
MUST_JOIN = os.getenv("MUST_JOIN", "").strip()
OWNER_ID_RAW = os.getenv("OWNER_ID", "").strip()

if not API_ID:
    raise SystemExit("No API_ID found. Exiting...")
elif not API_HASH:
    raise SystemExit("No API_HASH found. Exiting...")
elif not BOT_TOKEN:
    raise SystemExit("No BOT_TOKEN found. Exiting...")

try:
    API_ID = int(API_ID)
except ValueError:
    raise SystemExit("API_ID is not a valid integer. Exiting...")

try:
    OWNER_ID = int(OWNER_ID_RAW) if OWNER_ID_RAW else 0
except ValueError:
    raise SystemExit("OWNER_ID is not a valid integer. Exiting...")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
