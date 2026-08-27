# Duplicate Record Detection System

A 3rd-year Data Science / Data Engineering college project that detects duplicate and near-duplicate records in CSV datasets.

## Problem Statement

Real-world datasets often contain duplicate records caused by data entry errors, formatting differences, abbreviations, and missing values. For example, "Ravi Kumar" and "RAVI KUMAR" may refer to the same person, but a simple exact-match check will miss them.

## Objective

Build a practical system that:
- Inspects and preprocesses CSV data
- Detects exact and near-duplicate records
- Scores similarity using fuzzy matching, Jaccard, and TF-IDF
- Evaluates results against ground truth
- Presents findings in a simple Streamlit dashboard

## Dataset

- **sample_data.csv** — ~420 customer records with columns: `record_id`, `name`, `email`, `phone`, `address`, `city`, `pincode`
- **ground_truth.csv** — known duplicate pairs for evaluation

The dataset includes:
- True duplicates with formatting variations (names, phones, addresses)
- Similar-but-different records (e.g. "Ravi Kumar" vs "Ravi Kumari") to demonstrate false positives

## Methodology

```
Data
 ↓
Preprocessing
 ↓
Normalization
 ↓
Blocking
 ↓
Similarity
 ↓
Feature Engineering
 ↓
Scoring
 ↓
Classification
 ↓
Evaluation
```

## Technologies

- Python, Pandas, NumPy
- Scikit-learn (TF-IDF, cosine similarity)
- RapidFuzz (fuzzy string matching)
- Streamlit (dashboard)
- Plotly (charts)

## Project Structure

```
duplicate-record-detector/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── sample_data.csv
│   └── ground_truth.csv
├── src/
│   ├── preprocessing.py
│   ├── similarity.py
│   ├── matching.py
│   └── evaluation.py
└── outputs/
```

## Setup

```bash
pip install -r requirements.txt
python scripts/generate_dataset.py   # regenerate sample data if needed
streamlit run app.py
```

## Development Stages

| Stage | Status | Description |
|-------|--------|-------------|
| 1 | ✅ Done | Dataset + Data Inspection |
| 2 | Pending | Preprocessing + Normalization |
| 3 | Pending | Exact Duplicate Detection |
| 4 | Pending | Candidate Generation |
| 5 | Pending | Fuzzy + Jaccard Similarity |
| 6 | Pending | TF-IDF + Cosine Similarity |
| 7 | Pending | Feature Engineering + Scoring |
| 8 | Pending | Evaluation |
| 9 | Pending | Full Streamlit Dashboard |

## Results

*(To be filled after evaluation stage)*

## Limitations

*(To be filled after full implementation)*

## Future Improvements

*(To be filled after full implementation)*
