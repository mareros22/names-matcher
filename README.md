## Overview
Work-in-progress web application to help parents agree on baby names
### Setup
1. Create a virtual environment
   `py -3 -m venv .venv`
2. Activate the virtual environment
   `.venv\Scripts\activate`
3. Install dependencies
   `pip install flask`
   `pip install requests`
### Data Entry
Scraper: scrape data from downloaded Wikipedia and National Registry archives of baby names
  Usage: `python scraper.py`
Ingest: (in-progress) ingest scraped data to database
  Must initialize and run database first
  Usage: `python ingest.py`
### Flask backend
Must activate virtual environment venv with `.venv\Scripts\activate`
Initialize database: `flask --app flaskr init-db`
Run app: `flask --app flaskr run`
