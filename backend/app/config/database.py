from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://root:test1234@database.ohejniv.mongodb.net/?appName=database",
)

client = AsyncIOMotorClient(MONGO_URI)

db = client["faculty_appraisal"]

faculty_collection = db["faculty"]
criteria_collection = db["criteria"]
documents_collection = db["documents_metadata"]
scores_collection = db["scores"]
