from pymongo import MongoClient
import os
from dotenv import load_dotenv
from utils.logging_config import get_logger

logger = get_logger(__name__)

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["job-matching-system"]

# Check and create collections if they don't exist
try:
    existing_collections = db.list_collection_names()

    if "Users" not in existing_collections:
        db.create_collection("Users")
        logger.info("Users collection created successfully.")

    if "Rules" not in existing_collections:
        db.create_collection("Rules")
        logger.info("Rules collection created successfully.")

    if "Jobs" not in existing_collections:
        db.create_collection("Jobs")
        logger.info("Jobs collection created successfully.")

except Exception as e:
    logger.error(f"An error occurred while creating collections: {e}")