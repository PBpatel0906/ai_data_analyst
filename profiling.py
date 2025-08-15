import pandas as pd

def quick_profile(df: pd.DataFrame) -> dict:
    n_rows, n_cols = df.shape
    dtypes = {c: str(t) for c, t in df.dtypes.items()}
    missing = {c: int(df[c].isna().sum()) for c in df.columns}
    # simple numeric stats
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    stats = {}
    if numeric_cols:
        desc = df[numeric_cols].describe().to_dict()
        stats = {k: {m: float(v) for m, v in val.items()} for k, val in desc.items()}
    return {
        "n_rows": int(n_rows),
        "n_cols": int(n_cols),
        "columns": list(df.columns),
        "dtypes": dtypes,
        "missing": missing,
        "numeric_summary": stats,
    }