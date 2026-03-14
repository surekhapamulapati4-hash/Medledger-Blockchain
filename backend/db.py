import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["medchain_db"]

hospitals_collection = db["hospitals"]
reports_collection = db["reports"]
verification_logs = db["verification_logs"]
