from fastapi import APIRouter, HTTPException
from utils.logging_config import get_logger
from utils.models import Resume
from utils.db import get_db
from utils.utils import get_categories, get_category_rules_dict, process_matching
from services.openai import analyze_job_description

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
    
@router.post("/api/addCategory/{category}")
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
    

@router.get("/api/refreshPage")
async def refresh_page():
    logger.info("Refreshing page")
    job_desc = r"""This position is intended for students in a degree-seeking program to which they will return to school at the end of the summer internship in 2025, with a graduation date of Winter 2025 or later. If you do not meet these minimum criteria, please revisit our careers site for other opportunities. **

At Intuit, our engineers are the lifeblood of our success and we work hard to ensure they are doing the greatest work of their lives. Come join Intuit’s Core Services and Experiences Team as a Software Engineer Intern focusing on modern web application design and development. In this role you will be working on industry leading authentication (MFA via Biometric and password-less) methods to enable a frictionless user experience while keeping the bad guys out of Intuit products. We are also responsible for creating a world-class identity verification solution for Intuit to help the company's mission of powering prosperity around the world.

What you'll bring

(Must Have)

Working towards a Bachelor or Master’s degree in computer science or a related technical field
Solid understanding of object oriented design and programming languages.
Knowledge of front-end web design and modern JavaScript features such as ES6, ES7 & ES8
Strong design sense and ability to translate wire-frames, mockups and visual design assets to engaging and user-friendly web experiences using Photoshop, CSS, HTML and JavaScript.
Understanding of Test-Driven Development with experience creating JavaScript-based test coverage
An understanding of the Software Development Life Cycle (SDLC).
Experience with Agile Development, SCRUM, or Extreme Programming methodologies
"Self-starter"" attitude and ability to make decisions independently.
Helpful, can-do attitude and a willingness to take ownership of problems.
Strong desire to learn and grow.
Excellent problem solving skills with a history of superb delivery against assigned tasks.
Excellent verbal and written communication skills.

(Nice To Have)

Experience building modular JavaScript single-page applications with React, Redux, Webpack, Jest and Babel
Knowledge of AWS or other cloud computing services
Knowledge of Docker, Kubernetes, ECS, EKS
Ability to translate technical user requirements into world class visual designs

“The pay range for this position is: $35.50 - $55.50 (per hour), and varies based on education and location”

How you will lead

Designing and developing web apps, prototypes, or proofs of concepts
Ensuring code coverage is applied using latest UI testing frameworks and patterns
Resolve defects/bugs during QA testing, pre-production, production, and post-release patches 
Work cross-functionally with various Intuit teams including: product management, various product lines, and/or business units to drive forward results."""

    categories = get_categories()
    extracted_info = analyze_job_description(job_desc, categories)
    logger.debug(f"Extracted information from job description: {extracted_info}")

    category_rules_dict = get_category_rules_dict()
    match_percentage, matched_categories, similarity_results = process_matching(
        extracted_info, category_rules_dict, categories, threshold=0.75
    )

    logger.info(f"Match Percentage: {match_percentage}%")
    logger.info(f"Matched Categories: {matched_categories}")
    logger.info(f"Similarity Results: {similarity_results}")

    return {"status": "Page refreshed successfully", "match_percentage": match_percentage, "matched_categories": matched_categories}
