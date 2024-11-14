import os
from openai import OpenAI
from dotenv import load_dotenv
from utils.logging_config import get_logger
import json

load_dotenv()
logger = get_logger(__name__)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def analyze_job_description(description: str, categories: list):
    logger.info("Starting analysis of job description.")
    try:
        # Convert the list of categories to a comma-separated string
        categories_str = ', '.join(categories)

            # Create the prompt
        prompt = f"""
        Extract the following information from the job description based on these categories: [{categories_str}].

        For each category, provide a list of relevant information found in the job description.

        Return the results in the following JSON format:

        {{
            "Category1": "Extracted info 1, Extracted info 2",
            "Category2": "Extracted info 1, Extracted info 2",
            ...
        }}

        Ensure that the JSON is properly formatted and parsable.

        Job Description:
        \"\"\"
        {description}
        \"\"\"
        """
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that extracts structured information from job descriptions based on specified categories."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        logger.info("Received response from OpenAI.")

        content = response.choices[0].message.content.strip()
        extracted_info = json.loads(content)
        return extracted_info
    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        raise