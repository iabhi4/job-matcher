from fastapi import APIRouter, HTTPException
from db.mongo import db
from models.schemas import RuleSet
from utils.logging_config import get_logger
from typing import List
from pydantic import ValidationError

rulesRouter = APIRouter()
logger = get_logger(__name__)

@rulesRouter.post("/api/rules", response_model=dict)
async def add_rules(rule_set: RuleSet):
    """
    Endpoint to save all the rules created by the user in the database
    """
    logger.info(f"Received request to save rules for user: {rule_set.user_id}")
    try:
        rules_collection = db["Rules"]

        # Update existing rules or insert new ones
        result = rules_collection.update_one(
            {"user_id": rule_set.user_id},
            {"$set": rule_set.dict()},
            upsert=True
        )

        if result.upserted_id:
            logger.info(f"Rules created for user_id: {rule_set.user_id} with _id: {result.upserted_id}")
        else:
            logger.info(f"Rules updated for user_id: {rule_set.user_id}")

        return {"message": "Rules added/updated successfully!"}

    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=f"Validation error: {e}")

    except Exception as e:
        logger.error(f"Error saving rules: {str(e)}")
        raise HTTPException(status_code=500, detail="Error saving rules")

@rulesRouter.get("/api/rules/{user_id}", response_model=RuleSet)
async def get_rules(user_id: str):
    """
    Endpoint to get all the rules created by the user from the database
    """
    try:
        rules_data = db["Rules"].find_one({"user_id": user_id})
        if rules_data:
            logger.info(f"Rules retrieved for user_id: {user_id}")
            return RuleSet(**rules_data)  # Convert back to RuleSet model
        else:
            logger.info(f"No rules found for user_id: {user_id}")
            raise HTTPException(status_code=404, detail="No rules found")

    except Exception as e:
        logger.error(f"Error retrieving rules: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving rules")
    
def getAllRules(user_id: str):
    """
    Utility function to get all the rules created by the user from the database
    """
    try:
        rule_set = db["Rules"].find_one({"user_id": user_id})
        if rule_set:
            logger.info(f"Rules retrieved for user_id: {user_id}")
            rules = rule_set["rules"]
            rules_dict = {item['category']: item['rule'] for item in rules}
            rules_dict["len()"] = len(rules)
            return rules_dict
        else:
            logger.info(f"No rules found for user_id: {user_id}")
            raise HTTPException(status_code=404, detail="No rules found")

    except Exception as e:
        logger.error(f"Error retrieving rules: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving rules")