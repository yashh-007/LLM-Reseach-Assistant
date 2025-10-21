import pandas as pd
from pathlib import Path

CSV_FILE = Path("data/sjr_2024.csv")

def load_quartiles():
    """
    Load SJR CSV and return a dict: { "Journal Name": "Q1/Q2/Q3/Q4" }
    """
    if not CSV_FILE.exists():
        raise FileNotFoundError(f"{CSV_FILE} not found. Please download and save it in the data folder.")

    df = pd.read_csv(CSV_FILE)
    # Adjust column names based on your CSV
    # For SJR CSV: usually 'Title' and 'SJR Quartile'
    quartiles = dict(zip(df['Title'], df['SJR Quartile']))
    return quartiles
