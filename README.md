# LLM Research Assistant
**LLM Research Assistant** is a Streamlit web application that helps researchers search for academic papers and filter them based on journal quartiles (Q1/Q2) using SJR data. It provides an easy interface to find high-quality research papers by topic and publication year.  

## Features
- **Search Research Papers:** Search Google Scholar for papers by topic.  
- **Year Filter:** Filter papers by publication year using an interactive slider.  
- **Quartile Filter:** Option to display only Q1/Q2 journals based on SJR 2024 data.  
- **Paper Details:** View title, journal, year, quartile, and link to the paper.  

## Folder Structure
LLM-Research-Assistant/
├─ app.py
├─ requirements.txt
├─ data/
│ └─ sjr_2024.csv
├─ utils/
│ ├─ journal_filter.py
│ └─ sjr_quartiles.py


## Setup Instructions
1. **Clone the repository:**

git clone <your-repo-url>
cd LLM-Research-Assistant

2. Create and activate a virtual environment:
   python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

3. Install dependencies:
   pip install -r requirements.txt

4. Add SJR CSV file: Download the SJR 2024 CSV from Scimago Journal & Country Rank
 and place it in data/sjr_2024.csv.

5. Add your SerpAPI key (optional): If using SerpAPI for Google Scholar, add your API key in utils/journal_filter.py.

6. streamlit run app.py

Notes

Make sure the utils folder contains both journal_filter.py and sjr_quartiles.py.

Avoid uploading any API keys to GitHub.

The app fetches real-time results from Google Scholar (via SerpAPI), so results depend on your network and API limits.
