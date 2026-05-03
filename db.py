from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi

load_dotenv()
url = os.getenv("MONGO_DB_URL")
client = MongoClient(
    url,
    tlsCAFile=certifi.where(),
    tls=True
)
db = client["emosenseai"]
users_collection = db["users"]
history_collection = db["emotion_history"]