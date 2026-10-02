import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=True)

APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
APP_PORT = int(os.getenv("APP_PORT", "8000"))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

# Current model IDs are configurable through .env.
GEMINI_WORKOUT_MODEL = os.getenv("GEMINI_WORKOUT_MODEL", "gemini-3.1-pro-preview").strip()
GEMINI_FAST_MODEL = os.getenv("GEMINI_FAST_MODEL", "gemini-3.8-flash").strip()

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'fitbuddy.db'}")
