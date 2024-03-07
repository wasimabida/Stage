from scraping.scraping import scrape_facebook_posts_with_hashtag
from saving.save_csv import save_to_csv
from fast_api.app import app
import uvicorn 

if __name__ == "__main__":
    email = input("Enter your Facebook email: ")
    password = input("Enter your Facebook password: ")
    hashtag = input("Enter the hashtag you want to search for: ")

    # Démarrer le scraping
    pubs = scrape_facebook_posts_with_hashtag(email, password, hashtag)
    print(pubs)

    # Enregistrer dans CSV
    if pubs:
        save_to_csv(pubs)
        print("Posts have been successfully scraped and saved to a CSV file.")
    else:
        print("No posts were scraped.")

    # Démarrer l'application FastAPI
    uvicorn.run(app, host="0.0.0.0", port=8000)

