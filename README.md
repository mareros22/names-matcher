# Overview
Work-in-progress web application to help parents agree on baby names
## Setup
1. \[If necessary\] Create a virtual environment
   </br>
   `py -3 -m venv .venv`
3. Activate the virtual environment
   </br>
   `.venv\Scripts\activate`
5. Install dependencies
   </br>
   `pip install flask`
   </br>
   `pip install requests`
## Data Entry
### Scraper: scrape data from downloaded Wikipedia and National Registry archives of baby names
  Usage: `python scraper.py`
  
### Ingest: (in-progress) ingest scraped data to database
  Must initialize and run database first
  </br>
  Usage: `python ingest.py`
  </br>
## Flask backend
Must activate virtual environment venv with `.venv\Scripts\activate`
</br>
Initialize database: `flask --app flaskr init-db`
</br>
Run app: `flask --app flaskr run`
