"""
Duplicate Record Detection System — Streamlit Dashboard

Stage 1: Dataset loading and data inspection.
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.preprocessing import get_column_summary, inspect_data, load_csv

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Duplicate Record Detector",
    page_icon="🔍",
    layout="wide",
)

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_DATA = PROJECT_ROOT / "data" / "sample_data.csv"


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
st.sidebar.title("Duplicate Record Detector")
st.sidebar.markdown("A Data Science project for detecting duplicate records in CSV datasets.")
st.sidebar.markdown("---")
st.sidebar.markdown("**Stage 1:** Data Inspection")

uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

use_sample = st.sidebar.checkbox("Use sample dataset", value=True)


# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
@st.cache_data
def load_sample_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


df = None
if uploaded_file is not None:
    df = load_csv(uploaded_file=uploaded_file)
    st.sidebar.success("Uploaded file loaded.")
elif use_sample and DEFAULT_DATA.exists():
    df = load_sample_data(str(DEFAULT_DATA))
    st.sidebar.info("Using built-in sample dataset.")
else:
    st.warning("Please upload a CSV or enable the sample dataset.")
    st.stop()


# ---------------------------------------------------------------------------
# Main — Data Inspection
# ---------------------------------------------------------------------------
st.title("Duplicate Record Detection System")
st.markdown("### Stage 1 — Data Inspection")

st.info(
    "Before detecting duplicates, we inspect the dataset to understand its structure, "
    "missing values, and obvious problems. This is the first step in any Data Science pipeline."
)

# --- Overview metrics ---
inspection = inspect_data(df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Records", inspection["num_rows"])
col2.metric("Columns", inspection["num_columns"])
col3.metric("Missing Values", inspection["missing_values"])
col4.metric("Exact Duplicate Rows", inspection["exact_duplicate_count"])

st.markdown("---")

# --- Column info ---
st.subheader("Column Overview")
st.markdown(
    "Each column has a **data type** (e.g. `object` for text, `int64` for numbers). "
    "Understanding types helps decide how to preprocess each field."
)

summary_df = get_column_summary(df)
st.dataframe(summary_df, use_container_width=True, hide_index=True)

# --- Missing values chart ---
st.subheader("Missing Values by Column")
missing_df = pd.DataFrame([
    {"Column": col, "Missing Count": count}
    for col, count in inspection["missing_by_column"].items()
    if count > 0
])

if len(missing_df) > 0:
    fig_missing = px.bar(
        missing_df,
        x="Column",
        y="Missing Count",
        title="Missing / Empty Values per Column",
        color="Missing Count",
        color_continuous_scale="Reds",
    )
    st.plotly_chart(fig_missing, use_container_width=True)
else:
    st.success("No missing or empty values found in any column.")

# --- Data types ---
with st.expander("Data Types Detail"):
    dtype_df = pd.DataFrame([
        {"Column": col, "Data Type": dtype}
        for col, dtype in inspection["dtypes"].items()
    ])
    st.dataframe(dtype_df, hide_index=True)

# --- Exact duplicates ---
st.subheader("Exact Duplicate Rows")
st.markdown(
    "An **exact duplicate** means two rows are **completely identical** across all columns. "
    "Pandas finds these using `df.duplicated()`."
)

if inspection["exact_duplicate_count"] > 0:
    st.warning(
        f"Found **{inspection['exact_duplicate_count']}** rows that are exact duplicates "
        f"(including the first occurrence of each duplicate group)."
    )
    st.dataframe(inspection["exact_duplicate_rows"], use_container_width=True)
else:
    st.success(
        "No exact duplicate rows found. "
        "This is expected — our sample data has *near-duplicates* with formatting differences, "
        "not identical raw rows."
    )

# --- Sample preview ---
st.subheader("Sample Data Preview")
st.dataframe(inspection["sample_preview"], use_container_width=True)

# --- Learning box ---
with st.expander("📚 Stage 1 Learning Notes"):
    st.markdown("""
**What we did**
- Loaded a CSV into a Pandas DataFrame
- Counted rows, columns, missing values, and exact duplicates
- Displayed column types and a sample preview

**Why we did it**
- You cannot clean or match data you haven't understood first
- Inspection reveals data quality issues before any algorithm runs

**Data Science concepts**
- **DataFrame**: a 2D table (rows = records, columns = fields)
- **Missing values**: empty cells or blank strings that can break comparisons
- **Categorical vs numerical**: text fields (name, city) vs numbers (pincode)
- **Unique values**: how many distinct values a column has
- **Duplicate rows**: rows that are identical across all columns

**Simple example**
```
Row 1: Ravi, ravi@gmail.com, 9876543210
Row 2: Ravi, ravi@gmail.com, 9876543210   ← exact duplicate of Row 1
Row 3: RAVI KUMAR, ravi@gmail.com, +91-9876543210  ← NOT exact (different formatting)
```

**Important code**
```python
df = pd.read_csv("data/sample_data.csv")
df.shape                    # (rows, columns)
df.isnull().sum()           # missing per column
df.duplicated(keep=False)   # flag exact duplicate rows
df.dtypes                   # column data types
```

**What to remember**
- Always inspect data before processing
- Exact duplicates are easy; near-duplicates need similarity methods (later stages)

**Possible viva question**
- *Why is data inspection important before duplicate detection?*
  → It helps identify missing values, wrong data types, and the scale of the problem.
    Without inspection, preprocessing choices would be blind guesses.
""")
