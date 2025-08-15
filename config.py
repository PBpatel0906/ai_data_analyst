import os
from pathlib import Path

BASE_DIR = Path(_file_).resolve().parent.parent
DATA_DIR = BASE_DIR.parent / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# ensure dirs exist at import time
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

API_TITLE = "AI Data Analyst API"
API_VERSION = "0.1.0"