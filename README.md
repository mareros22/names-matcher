## Overview
Work-in-progress web application to help parents agree on baby names
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
