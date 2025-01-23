from pymongo import MongoClient
from bson.objectid import ObjectId


class Mongo_Client:
    def __init__(self, mongo_uri):
        try:
            client = MongoClient(mongo_uri)
            self.db = client["media_scribe"]

            self.sessions_collection = self.db["sessions"]

            self.knowledge_collection = self.db["knowledges"]

        except Exception as e:

            print(f"Error in init {e}")

    def create_session(self, knowledge):
        try:
            session = {"messages": [], "knowledge": knowledge}
            result = self.sessions_collection.insert_one(session)
            return result.inserted_id
        except Exception as e:
            print(f"Error in create {e}")

    def update_index(self, knowledge_name):

        knowledge = knowledge_name.split("_extraction")[0]

        self.knowledge_collection.update_one(
            {"knowledge_name": knowledge},
            {"$set": {"ready": str(True)}},
        )

    def add_message(self, session_id, question, content):
        try:

            message = [question, content]

            # message = {"role": role, "content": content}
            self.sessions_collection.update_one(
                {"_id": ObjectId(session_id)}, {"$push": {"messages": message}}
            )
        except Exception as e:
            print(f"Fail adding message: {e}")

    # def add_message(self, session_id, role, content):
    #    try:

    #        message = {"role": role, "content": content}
    #        self.sessions_collection.update_one(
    #            {"_id": ObjectId(session_id)}, {"$push": {"messages": message}}
    #        )
    #    except Exception as e:
    #        print(f"Fail adding message: {e}")

    def get_session_history(self, session_id):
        try:
            session = self.sessions_collection.find_one({"_id": ObjectId(session_id)})
            if session:
                return session.get("messages")

            return []
        except Exception as e:
            print(f"error get session history: {e}")

    def get_session_knowledge(self, session_id):
        try:
            session = self.sessions_collection.find_one({"_id": ObjectId(session_id)})
            if session:
                return session.get("knowledge")

            return []
        except Exception as e:
            print(f"error get session knowledge: {e}")

    def get_session_messages(self, session_id):
        try:
            session = self.sessions_collection.find_one({"_id": ObjectId(session_id)})
            if session:
                return session.get("messages")

            return []
        except Exception as e:
            print(f"error get session knowledge: {e}")

    def get_all_sessions(self):

        try:
            sesions = list(self.sessions_collection.find({}, {"messages": 0}))

            sesions_json = [
                {
                    "id": str(field["_id"]),
                    **{k: field[k] for k in field if k != "_id"},
                }
                for field in sesions
            ]

            return sesions_json

        except Exception as e:
            print(f"Error calling all {e}")
