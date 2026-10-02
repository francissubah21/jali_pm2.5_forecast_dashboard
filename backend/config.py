import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.getenv("DATA_DIR", BASE_DIR / "data"))

STALE_AFTER_DAYS = int(os.getenv("STALE_AFTER_DAYS", "30"))
WHO_PM25_24H = float(os.getenv("WHO_PM25_24H", "15"))

APP_TITLE = os.getenv(
    "APP_TITLE",
    "Jali Station — PM2.5 Forecast Dashboard"
)
