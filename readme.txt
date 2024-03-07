Description:
This project consists of two main parts:

    -Web Scraping: Scrapes posts from social media platforms (Facebook) with the tag #harcèlement and stores them in a CSV file.
    -FastAPI Application: Provides endpoints to clean the comments, analyze their toxicity using the Detoxify model, and store the data in MongoDB.

tap these commands at first :

    pip install requests pymongo beautifulsoup4
    pip install fastapi
    pip install uvicorn
    pip install detoxify (pour le modele d'anlyse)

run the project: 

    python main.py

