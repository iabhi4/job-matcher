from fastapi import APIRouter, HTTPException
from db.mongo import db
from models.schemas import User, Resume
from utils.logging_config import get_logger
from typing import Dict, List

userRouter = APIRouter()
logger = get_logger(__name__)

@userRouter.get("/api/users/names", response_model=List[str])
async def get_all_user_names():
    """
    Endpoint to get all user names from the database, This endpoint is not integral for the
    project, Added to speed up the demo process
    """
    logger.info("Received request to get all user names")
    try:
        user_collection = db["Users"]
        names = [user["name"] for user in user_collection.find({}, {"name": 1})]
        logger.info(f"Retrieved {len(names)} user names")
        return names
    except Exception as e:
        logger.error(f"Error retrieving user names: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving user names")

@userRouter.get("/api/users/{name}", response_model=User)
async def get_user(name: str):
    """
    Endpoint to get the user personal and resume data from the database
    """
    logger.info(f"Received request to get user: {name}")
    try:
        user_data = db["Users"].find_one({"name": name})
        if user_data:
            logger.info(f"User found: {name}")
            user_data["_id"] = str(user_data["_id"])
            return user_data
        else:
            logger.info(f"User not found: {name}")
            raise HTTPException(status_code=404, detail="User not found")

    except Exception as e:
        logger.error(f"Error retrieving user: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving user")

@userRouter.post("/api/save_user", response_model=dict)
async def save_user(data: Dict):
    """
    Endpoint to save user personal and resume data to the database
    """
    logger.info("Received request to create or update user")
    try:
        user_collection = db["Users"]

        name = data.get("name")
        resume_data = data.get("resume")

        if not name or not resume_data:
            raise HTTPException(status_code=400, detail="Name and resume data are required")

        resume = Resume(**resume_data)
        user = User(name=name, resume=resume)

        # Find and update or insert if not found
        update_result = user_collection.update_one(
            {"name": name},
            {"$set": user.dict()},
            upsert=True
        )

        if update_result.upserted_id:
            logger.info(f"User created: {name} with _id: {update_result.upserted_id}")
            return {"message": "User created successfully"}
        elif update_result.modified_count > 0:
            logger.info(f"User updated: {name}")
            return {"message": "User updated successfully"}
        else:
            logger.info(f"User details unchanged: {name}")
            return {"message": "User details unchanged"}

    except Exception as e:
        logger.error(f"Error saving user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error saving user: {str(e)}")
    
def getResumeData(name: str):
    """
    Utility function to fetch resume data for a user from the database
    """
    logger.info(f"Fetching resume data for user: {name}")
    try:
        user_collection = db["Users"]
        resume_data = user_collection.find_one({"name": name})
        if resume_data:
            logger.info(f"Resume data found for user: {name}")
            resume = str(resume_data["resume"])
            return resume
        else:
            logger.info(f"No resume data found for user: {name}")
            return None
    except Exception as e:
        logger.error(f"Error fetching resume data for user {name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching resume data for user {name}: {str(e)}")