from fastapi import APIRouter, HTTPException, Request
from db.mongo import db
from utils.logging_config import get_logger
from typing import List, Dict
from models.schemas import Job
from routes.rules import getAllRules
from routes.user import getResumeData
from services.openai import analyze_job_description
from utils.prolog import prolog_matching
import json
from bson import ObjectId

dashboardRouter = APIRouter()
logger = get_logger(__name__)

@dashboardRouter.get("/api/jobs", response_model=List[Dict])
async def get_matched_jobs():
    """
    Get all jobs that have been analyzed from the DB
    """
    logger.info("Received request to get matched jobs")
    try:
        jobs_collection = db["Jobs"]
        matched_jobs = list(jobs_collection.find({}))

        for job in matched_jobs:
            job["id"] = str(job["_id"])
            del job["_id"]

        logger.info(f"Retrieved {len(matched_jobs)} matched jobs")
        return matched_jobs
    except Exception as e:
        logger.error(f"Error retrieving matched jobs: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving matched jobs")
    
@dashboardRouter.get("/api/getJob/{job_id}", response_model=Job)
async def get_job(job_id):
    """
    Get the Job object for a specific id requested by frontend for the card view popup
    """
    logger.info(f"Received request to get job with ID: {job_id}")
    try:
        jobs_collection = db["Jobs"]
        job = jobs_collection.find_one({"_id": ObjectId(job_id)})

        if job:
            # Convert ObjectId to string for JSON serialization
            job["id"] = str(job["_id"])
            del job["_id"]

            logger.info(f"Found job with ID: {job_id}")
            return job
        else:
            logger.warning(f"Job with ID: {job_id} not found")
            raise HTTPException(status_code=404, detail="Job not found")

    except Exception as e:
        logger.error(f"Error retrieving job: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving job")
    
@dashboardRouter.post("/api/analyze", response_model=Dict)
async def analyze(request: Request):
    """
    Main endpoint of the project where all the NLP extraction and Prolog matching is done
    We are also storing the analyzed job in the database here
    """
    logger.info("Received request to analyze job description")
    try:
        data = await request.json()
        companyName = data.get("companyName")
        jobDescription = data.get("jobDescription")
        logger.info("Fetching rules from the database")
        rules = getAllRules("Abhinav Sin")

        # Get Resume from the database
        logger.info("Fetching resume from the database")
        resume = getResumeData("Abhinav Sin")

        logger.info("Analyzing job description")
        extracted_info = analyze_job_description(jobDescription, rules, resume)
        logger.info("Back to Dashboard after OpenAI analysis", type(extracted_info))
        extracted_info = json.loads(extracted_info)
        logger.info("Back to Dashboard after OpenAI analysis", extracted_info)
        prolog_info = extracted_info["prolog"]
        logger.info("Extracted Prolog info: %s", prolog_info)
        resume_info = extracted_info["resume"]
        job_info = extracted_info["job_metadata"]

        logger.info("Performing prolog matching")
        prolog_result = prolog_matching(rules, prolog_info)

        logger.info("Creating job object")
        detailed_analysis = {
            "prolog_analysis": {
                "matched_rules": prolog_result["matched_rules"],
                "score": prolog_result["score"]
            },
            "resume_analysis": {
                "matched_keywords": resume_info.get("matches", []),
                "score": len(resume_info.get("matches", [])) * 5  # Assuming 5 points per match
            }
        }
        job = Job(
            userId="Abhinav Sin",
            companyName=companyName,
            jobTitle=job_info.get("job_position", "Unknown"),
            location=job_info.get("job_location", "Unknown"),
            matchScore=int(prolog_result["score"]) + (len(resume_info["matches"]) * 5),  # Use the score from prolog_result
            companyLogo=None,  # Placeholder for company logo
            detailedAnalysis=detailed_analysis
        )
        job_dict = job.dict()

        logger.info("Inserting job analysis into the database")
        jobs_collection = db["Jobs"]
        result = jobs_collection.insert_one(job_dict)

        logger.info(f"Job analysis saved with ID: {result.inserted_id}")
        return {"message": "Job analysis saved", "job_id": str(result.inserted_id)}
    except Exception as e:
        logger.error(f"Error analyzing job description: {str(e)}")
        raise HTTPException(status_code=500, detail="Error analyzing job description")