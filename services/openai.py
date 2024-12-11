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

def clean_response(content):
    content = content.strip()
    if content.startswith('```') and content.endswith('```'):
        content = content[content.find('\n')+1:content.rfind('```')].strip()
    content = content.strip()
    try:
        start = content.index('{')
        end = content.rindex('}') + 1
        json_str = content[start:end]
        return json_str
    except ValueError:
        logger.error("No JSON object found in the assistant's response.")
        return None

def analyze_job_description(description: str, categories: list):
    logger.info("Starting analysis of job description.")
    try:
        categories_str = ', '.join(categories)

        prompt = f"""
You are an assistant that extracts key information from job descriptions based on specified categories. Your task is to extract concise, relevant data for each category, focusing on specific keywords and phrases rather than full sentences or paragraphs.

**Categories**: [{categories_str}]

**Instructions**:
- For each category, extract only the specific items or keywords relevant to that category.
- Do not include full sentences, bullet points, or any additional commentary.
- Present the extracted information as a list of items for each category.
- Avoid duplicate entries in the lists.
- If a category has no relevant information, include it with an empty list.
- Use **valid JSON format** with double quotes for keys and string values.
- **Do not include any text outside of the JSON output.**
- **Do not include any markdown formatting like code blocks or code fences in the output.**

**Format**:
{{
  "Category1": ["Item1", "Item2", "Item3"],
  "Category2": ["Item1", "Item2"],
  "Category3": []
}}

**Example**:

*Given the category "Skills" and a job description mentioning "Experience with Python, Java, and SQL", the extracted information should be:*

{{
  "Skills": ["Python", "Java", "SQL"]
}}

**Job Description**:
\"\"\"
{description}
\"\"\"
"""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that extracts key information from job descriptions based on specified categories."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        logger.info("Received response from OpenAI.")

        content = response.choices[0].message.content.strip()
        logger.debug(f"OpenAI response content: {content}")

        json_content = clean_response(content)
        if json_content:
            extracted_info = json.loads(json_content)
            return extracted_info
        else:
            raise ValueError("Assistant's response did not contain valid JSON.")

    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding failed: {e}")
        logger.debug(f"Response content that caused the error: {content}")
        raise
    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        raise