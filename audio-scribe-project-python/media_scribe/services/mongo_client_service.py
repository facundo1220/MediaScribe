from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime


class Mongo_Client:
    def __init__(self, mongo_uri):
        try:
            client = MongoClient(mongo_uri)
            self.db = client["media_scribe"]

            self.knowledge_collection = self.db["knowledges"]

        except Exception as e:

            print(f"Error in init {e}")

    def create_knowledge(self, knowledge, type):
        try:
            new_knowledge = {
                "knowledge_name": knowledge,
                "type": type,
                "created_at": datetime.today().replace(microsecond=0).isoformat(),
                "ready": str(False),
            }
            result = self.knowledge_collection.insert_one(new_knowledge)
            return result.inserted_id
        except Exception as e:
            print(f"Error in create {e}")

    def get_all_knowledges(self):

        try:
            knowledges = list(self.knowledge_collection.find())

            knowledges_json = [
                {
                    "id": str(field["_id"]),
                    **{k: field[k] for k in field if k != "_id"},
                }
                for field in knowledges
            ]

            return knowledges_json

        except Exception as e:
            print(f"Error calling all {e}")
