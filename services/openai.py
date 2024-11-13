import os
from openai import OpenAI
from dotenv import load_dotenv
from utils.logging_config import get_logger

load_dotenv()
logger = get_logger(__name__)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def analyze_job_description(description: str):
    logger.info("Starting analysis of job description.")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts keywords from job descriptions."},
                {"role": "user", "content": f"Extract key skills and requirements from this job description: {description}"}
            ]
        )
        logger.info("Received response from OpenAI.")
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        raise