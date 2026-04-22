from __future__ import annotations

import math
from datetime import date, datetime
from typing import Any

import pandas as pd


def _sanitize_value(val: Any) -> Any:
    if val is None:
        return None
    if isinstance(val, float) and math.isnan(val):
        return None
    try:
        if pd.isna(val):
            return None
    except (TypeError, ValueError):
        pass

    if hasattr(val, "item"):
        return val.item()

    if isinstance(val, pd.Timestamp):
        return val.isoformat() if not pd.isnull(val) else None

    if isinstance(val, (date, datetime)):
        return val.isoformat()

    return val


def dataframe_to_json_records(df: pd.DataFrame | None) -> list[dict[str, Any]]:
    if df is None or df.empty:
        return []

    records = []
    for _, row in df.iterrows():
        record = {col: _sanitize_value(row[col]) for col in df.columns}
        records.append(record)

    return records
