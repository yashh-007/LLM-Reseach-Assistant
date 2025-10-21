import pandas as pd
from pathlib import Path

CSV_FILE = Path("data/sjr_2024.csv")

def load_quartiles():
    """
    Load journal quartiles from the downloaded SJR CSV (semicolon-separated, no headers).
    Returns a dict: { "Journal Name": "Q1/Q2/Q3/Q4" }
    """
    df = pd.read_csv(CSV_FILE, sep=';', header=None, dtype=str)
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Detect SJR Best Quartile column (Q1-Q4)
    quartile_col = None
    for col in df.columns:
        if df[col].str.match(r'Q[1-4]').any():
            quartile_col = col
            break
    if quartile_col is None:
        raise ValueError("Could not detect SJR Best Quartile column.")

    # Detect journal title column (first non-empty in same row)
    first_row = df.iloc[0]
    title_col = None
    for col in df.columns:
        if col != quartile_col and first_row[col]:
            title_col = col
            break
    if title_col is None:
        raise ValueError("Could not detect journal title column.")

    return pd.Series(df[quartile_col].values, index=df[title_col]).to_dict()

if __name__ == "__main__":
    quartiles = load_quartiles()
    print(list(quartiles.items())[:10])
