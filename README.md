# LLM Research Assistant

**LLM Research Assistant** is a Streamlit web application that helps researchers search for academic papers and filter them based on journal quartiles (Q1/Q2) using SJR data. It provides an easy interface to find high-quality research papers by topic and publication year.

---

## Features

- **Search Research Papers:** Search Google Scholar for papers by topic.  
- **Year Filter:** Filter papers by publication year using an interactive slider.  
- **Quartile Filter:** Option to display only Q1/Q2 journals based on SJR 2024 data.  
- **Paper Details:** View title, journal, year, quartile, and link to the paper.  

---

## Folder Structure

LLM-Research-Assistant/
├─ app.py
├─ requirements.txt
├─ data/
│ └─ sjr_2024.csv
├─ utils/
│ ├─ journal_filter.py
│ └─ sjr_quartiles.py

yaml
Copy code

---

## Setup Instructions

1. **Clone the repository:**

```bash
git clone <your-repo-url>
cd LLM-Research-Assistant
Create and activate a virtual environment:


Copy code
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
Install dependencies:


Copy code
pip install -r requirements.txt
Add SJR CSV file:
Download the SJR 2024 CSV from Scimago Journal & Country Rank and place it in data/sjr_2024.csv.

If using SerpAPI for Google Scholar, add your API key in utils/journal_filter.py.

Running the App
bash
Copy code
streamlit run app.py
Open the URL displayed in the terminal (usually http://localhost:8501) to access the app.


The app fetches real-time results from Google Scholar (via SerpAPI), so results depend on your network and API limits.# LLM-Reseach-Assistant
