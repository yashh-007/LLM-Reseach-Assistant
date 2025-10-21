from Bio import Entrez
import os
import json
from dotenv import load_dotenv

# Load API keys
load_dotenv()
Entrez.email = os.getenv("ENTREZ_EMAIL")
Entrez.api_key = os.getenv("ENTREZ_API_KEY")

def fetch_pubmed(query, max_results=20, start_year=None, end_year=None):
    """
    Fetch PubMed papers metadata by query.
    Returns list of dicts: title, authors, journal, year, pubmed_link
    """
    search_args = {"term": query, "retmax": max_results}
    if start_year or end_year:
        year_filter = ""
        if start_year: year_filter += f"{start_year}[PDAT]:"
        else: year_filter += "1800[PDAT]:"
        if end_year: year_filter += f"{end_year}[PDAT]"
        else: year_filter += "3000[PDAT]"
        search_args["term"] += f" AND ({year_filter})"

    handle = Entrez.esearch(db="pubmed", **search_args)
    record = Entrez.read(handle)
    handle.close()
    id_list = record["IdList"]

    papers = []
    if not id_list:
        return papers

    handle = Entrez.efetch(db="pubmed", id=",".join(id_list), retmode="xml")
    records = Entrez.read(handle)
    handle.close()

    for item in records["PubmedArticle"]:
        art = item["MedlineCitation"]["Article"]
        authors = []
        for a in art.get("AuthorList", []):
            name = a.get("LastName", "") + " " + a.get("Initials", "")
            authors.append(name.strip())
        journal = art.get("Journal", {}).get("Title", "")
        pub_year = art.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {}).get("Year", "")
        title = art.get("ArticleTitle", "")
        pubmed_link = f"https://pubmed.ncbi.nlm.nih.gov/{item['MedlineCitation']['PMID']}/"
        papers.append({
            "title": title,
            "authors": authors,
            "journal": journal,
            "year": pub_year,
            "pubmed_link": pubmed_link
        })

    return papers

# Example usage
if __name__ == "__main__":
    query = "bladder cancer"
    papers = fetch_pubmed(query, max_results=5, start_year=2020, end_year=2025)
    print(json.dumps(papers, indent=2))
