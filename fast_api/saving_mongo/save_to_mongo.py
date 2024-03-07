import os
from dotenv import load_dotenv
from pymongo import MongoClient

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
            return result
        except Exception as e:
            return f"An error occurred: {e}"

    def get_from_mongodb(self):
        try:
            data = list(self.collection.find({}))
            return data
        except Exception as e:
            return f"An error occurred: {e}"

