from uuid import uuid4
from pathlib import Path
import pandas as pd
from typing import Tuple
from app.config import RAW_DIR

ALLOWED_EXT = {".csv", ".xlsx", ".xls"}

def save_upload_to_disk(file_bytes: bytes, original_name: str) -> Path:
    ext = Path(original_name).suffix.lower()
    if ext not in ALLOWED_EXT:
        raise ValueError(f"Unsupported file type: {ext}. Allowed: {ALLOWED_EXT}")
    dataset_id = f"{uuid4().hex}{ext}"
    dest = RAW_DIR / dataset_id
    dest.write_bytes(file_bytes)
    return dest

def read_dataframe(file_path: Path) -> pd.DataFrame:
    ext = file_path.suffix.lower()
    if ext == ".csv":
        return pd.read_csv(file_path)
    elif ext in {".xlsx", ".xls"}:
        return pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported extension: {ext}")

def sample_preview(df: pd.DataFrame, n: int = 20) -> list[dict]:
    # convert small preview to records for JSON
    return df.head(n).to_dict(orient="records")