import csv
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from dotenv import load_dotenv
from detoxify import Detoxify
import re
import os
from saving_mongo.save_to_mongo import MongoDBHandler
from analysis.analyze import analyze_toxicity
from cleaning.clean import clean


#ces lignes de codes ci-dessous presente le contenu des 3 derniers lignes d'imporation ci-dessus
"""
def analyze_toxicity(comment):
    # Initialize the Detoxify model
    model = Detoxify('original')
    
    # Analyze toxicity of the comment
    results = model.predict(comment)

    return results

def clean(comment):
    
    # Supprimer la ponctuation
    comment = re.sub(r'[^\w\s]', '', comment)
    
    # Supprimer les URLs
    comment = re.sub(r'http\S+', '', comment)

    # Convertir en minuscules
    comment = comment.lower()

    return comment

class MongoDBHandler:
    def __init__(self):
        self.load_env()
        self.client = MongoClient(self.mongodb_host, self.mongodb_port)
        self.db = self.client[self.mongodb_db]
        self.collection = self.db[self.mongodb_collection]

    def load_env(self):
        load_dotenv()
        self.mongodb_host = os.getenv("MONGODB_HOST")
        self.mongodb_port = int(os.getenv("MONGODB_PORT"))
        self.mongodb_db = os.getenv("MONGODB_DB")
        self.mongodb_collection = os.getenv("MONGODB_COLLECTION")

    def save_to_mongodb(self, comments):
        try:
            result = self.collection.insert_many(comments)
            return f"{len(result.inserted_ids)} comments saved to MongoDB"
        except Exception as e:
            return f"An error occurred: {e}"

    def get_from_mongodb(self):
        try:
            data = list(self.collection.find({}))
            return data
        except Exception as e:
            return f"An error occurred: {e}"
    
"""

app = FastAPI()

@app.post("/analyze_comments/")
async def analyze_comments_from_csv(filename: str = 'posts.csv'):
    # Charger les commentaires à partir du fichier CSV
    try:
        with open(filename, 'r', encoding='utf-8') as csvfile:
            comments = [row['text'] for row in csv.DictReader(csvfile)]
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Le fichier CSV spécifié n'a pas été trouvé.")

    # Nettoyer, analyser la toxicité et stocker les commentaires dans MongoDB
    cleaned_toxic_comments = []
    db_handler = MongoDBHandler()

    for comment in comments:
        cleaned_comment = clean(comment)
        toxicity_score = analyze_toxicity(cleaned_comment)
        cleaned_toxic_comments.append({"text": cleaned_comment, "toxicity_score": toxicity_score})

    # Stocker les commentaires nettoyés et leurs scores de toxicité dans MongoDB
    try:
        result = db_handler.save_to_mongodb(cleaned_toxic_comments)
        inserted_ids = [str(id) for id in result.inserted_ids]

        return {"message": "Les commentaires ont été analysés et stockés dans MongoDB avec succès.", "inserted_ids": inserted_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Une erreur s'est produite lors du stockage des commentaires dans MongoDB : {str(e)}")
