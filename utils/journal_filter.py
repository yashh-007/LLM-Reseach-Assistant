from serpapi import GoogleSearch
from pathlib import Path
import pandas as pd

# Load SJR CSV once
SJR_CSV = Path("data/sjr_2024.csv")
df_sjr = pd.read_csv(SJR_CSV, sep=";", header=None, dtype=str)
df_sjr = df_sjr.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Detect columns
quart_col = next((c for c in df_sjr.columns if df_sjr[c].str.match(r'Q[1-4]').any()), None)
title_col = next((c for c in df_sjr.columns if c != quart_col and df_sjr[c].iloc[0]), None)
quartiles_dict = pd.Series(df_sjr[quart_col].values, index=df_sjr[title_col]).to_dict()


def get_quartile(journal_name):
    journal_name = journal_name.lower()
    for sjr_journal, q in quartiles_dict.items():
        if sjr_journal.lower() in journal_name or journal_name in sjr_journal.lower():
            return q
    return "N/A"


def search_scholar(query, max_results=10, year_range=None):
    params = {
        "engine": "google_scholar",
        "q": query,
        "api_key": "3e7da2a77c84f7363703b3febd0b5c5c7b47c4ea9d554ab94605662a8f2885a8",
        "num": max_results,
    }
    if year_range:
        params["as_ylo"], params["as_yhi"] = year_range

    search = GoogleSearch(params)
    results = search.get_dict()

    papers = []
    for res in results.get("organic_results", []):
        pub_info = res.get("publication_info", {})
        # Extract authors properly
        authors_list = pub_info.get("authors", [])
        authors_str = ", ".join(a.get("name", "") for a in authors_list) if authors_list else "N/A"

        p = {
            "title": res.get("title"),
            "link": res.get("link"),
            "snippet": res.get("snippet"),
            "journal": pub_info.get("summary", ""),
            "year": pub_info.get("year", ""),
            "authors": authors_str,  # properly set authors
        }
        p["quartile"] = get_quartile(p["journal"])
        papers.append(p)

    return papers
