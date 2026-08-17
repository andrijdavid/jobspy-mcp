"""Tests for DataFrame serialization."""

from datetime import date

import pandas as pd
import pytest

from jobspy_mcp.serializer import dataframe_to_json_records


def test_empty_dataframe():
    assert dataframe_to_json_records(pd.DataFrame()) == []


def test_none_returns_empty():
    assert dataframe_to_json_records(None) == []


def test_nan_becomes_none():
    df = pd.DataFrame([{"salary": float("nan"), "title": "Engineer"}])
    records = dataframe_to_json_records(df)
    assert records[0]["salary"] is None
    assert records[0]["title"] == "Engineer"


def test_date_becomes_iso_string():
    df = pd.DataFrame([{"date_posted": date(2024, 1, 15)}])
    records = dataframe_to_json_records(df)
    assert records[0]["date_posted"] == "2024-01-15"


def test_timestamp_becomes_iso_string():
    df = pd.DataFrame([{"date_posted": pd.Timestamp("2024-01-15")}])
    records = dataframe_to_json_records(df)
    assert records[0]["date_posted"] == "2024-01-15T00:00:00"


def test_numpy_int_becomes_python_int():
    import numpy as np

    df = pd.DataFrame([{"count": np.int64(42)}])
    records = dataframe_to_json_records(df)
    assert records[0]["count"] == 42
    assert isinstance(records[0]["count"], int)


def test_multiple_rows():
    df = pd.DataFrame([
        {"title": "Engineer", "salary": 100_000},
        {"title": "Manager", "salary": float("nan")},
    ])
    records = dataframe_to_json_records(df)
    assert len(records) == 2
    assert records[1]["salary"] is None


def test_pandas_na_becomes_none():
    df = pd.DataFrame([{"value": pd.NA}])
    records = dataframe_to_json_records(df)
    assert records[0]["value"] is None
