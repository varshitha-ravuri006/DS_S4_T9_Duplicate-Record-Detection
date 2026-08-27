"""
Data inspection utilities.

Before preprocessing or matching, we inspect the dataset to understand
its shape, types, missing values, and obvious duplicate rows.
"""

import pandas as pd


def load_csv(file_path: str | None = None, uploaded_file=None) -> pd.DataFrame:
    """
    Load a CSV from disk or from a Streamlit uploaded file object.
    """
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    if file_path is not None:
        return pd.read_csv(file_path)
    raise ValueError("Provide either file_path or uploaded_file")


def inspect_data(df: pd.DataFrame) -> dict:
    """
    Run basic data inspection and return a summary dictionary.

    Returns
    -------
    dict with keys:
        num_rows, num_columns, columns, dtypes, missing_values,
        missing_by_column, exact_duplicate_rows, exact_duplicate_count,
        sample_preview
    """
    # Total missing cells across the whole DataFrame
    total_missing = int(df.isnull().sum().sum())

    # Also count empty strings as missing (common in CSV data)
    empty_string_count = 0
    for col in df.columns:
        if df[col].dtype == object:
            empty_string_count += (df[col].astype(str).str.strip() == "").sum()
    total_missing += empty_string_count

    # Exact duplicate rows (all columns identical)
    exact_dup_mask = df.duplicated(keep=False)
    exact_duplicate_count = int(exact_dup_mask.sum())

    missing_by_column = {}
    for col in df.columns:
        null_count = int(df[col].isnull().sum())
        if df[col].dtype == object:
            null_count += int((df[col].astype(str).str.strip() == "").sum())
        missing_by_column[col] = null_count

    # Unique value counts — useful to spot categorical vs high-cardinality fields
    unique_counts = {col: int(df[col].nunique(dropna=False)) for col in df.columns}

    return {
        "num_rows": len(df),
        "num_columns": len(df.columns),
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": total_missing,
        "missing_by_column": missing_by_column,
        "unique_counts": unique_counts,
        "exact_duplicate_rows": df[exact_dup_mask].copy(),
        "exact_duplicate_count": exact_duplicate_count,
        "sample_preview": df.head(10),
    }


def get_column_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a per-column summary table for display in the dashboard.
    """
    rows = []
    for col in df.columns:
        null_count = int(df[col].isnull().sum())
        empty_count = 0
        if df[col].dtype == object:
            empty_count = int((df[col].astype(str).str.strip() == "").sum())

        rows.append({
            "Column": col,
            "Data Type": str(df[col].dtype),
            "Non-Null Count": int(df[col].notna().sum()),
            "Missing / Empty": null_count + empty_count,
            "Unique Values": int(df[col].nunique(dropna=False)),
        })

    return pd.DataFrame(rows)
