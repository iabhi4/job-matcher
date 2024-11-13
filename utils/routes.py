from fastapi import APIRouter, HTTPException
from utils.logging_config import get_logger
from utils.models import Resume
from utils.db import get_db

logger = get_logger(__name__)
router = APIRouter()
db = get_db()

@router.post("/api/resume")
async def save_resume(resume: Resume):
    logger.info("Received resume for saving")
    try:
        resume_collection = db['resume_db']
        resume_collection.insert_one(resume.dict())
        logger.info("Resume saved successfully")
        return {"status": "Resume saved successfully"}
    except Exception as e:
        logger.error(f"Error saving resume: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/api/addCategory/{category}")
async def add_category(category: str, rule: str):
    logger.info(f"Adding category: {category} with rule: {rule}")
    try:
        category_collection = db['categories']
        category_collection.insert_one({"category": category, "rule": rule})
        logger.info("Category added successfully")
        return {"status": "Category added successfully"}
    except Exception as e:
        logger.error(f"Error adding category: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))