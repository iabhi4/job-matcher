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
    """
    Utility function to clean the assistant's response and extract the JSON object.
    """
    logger.info(f"Original content from OpenAI: {content}")
    content = content.strip()

    while content.startswith(("'", '"')) and content.endswith(("'", '"')):
        content = content[1:-1].strip()

    if content.startswith('```') and content.endswith('```'):
        content = content[content.find('\n') + 1:content.rfind('```')].strip()

    logger.info(f"Cleaned content: {content}")

    try:
        json_obj = json.loads(content)
        logger.info("Successfully parsed content as JSON.")
        return json.dumps(json_obj)
    except json.JSONDecodeError as e:
        logger.error(f"Content is not a valid JSON: {e}")
        return None
    
def analyze_job_description(description, user_rules, resume_data):
    """Analyze job description using GPT to extract the relevant information."""
    logger.info("Starting analysis of job description.")
    prompt = f"""You are an assistant that processes a job description and a resume to extract relevant information based on specified rules and categories. Your task is to analyze the provided job description and resume and return a structured JSON with three main keys:

1. **Prolog**: Analyze the job description based on provided Prolog rules. If the job description talks about these rules in any way, output the exact string written in the rule. For "Compensation" or "Pay" rules, if the numeric difference between values in the rule and the job description is less than $5000, also output the exact string written in the rule. If no match is found, return an empty string for that rule.

2. **Resume**: This includes a single aggregated list of keywords, phrases, or contextual matches from the resume that align semantically with the job description and categories.

3. **Job Metadata**:
   - **job_location**: Extract the job location from the job description. If the job location is not specified, set it as "Not Specified".
   - **job_position**: Extract the job title or position from the job description. Provide it as a single string.

---

### **Instructions**:
- Use **valid JSON format** with double quotes for keys and string values.
- **Do not include any text outside of the JSON output.**
- **Do not include any markdown formatting like code blocks or code fences in the output.**

#### **Prolog Key**:
- Use the provided Prolog rules to analyze the job description.
- For each rule:
  - If the job description mentions the rule in any way, include the **exact string** from the rule in the output JSON.
  - For "Compensation" or "Pay" rules:
    - If the numeric difference between values in the job description and the rule is less than $5000, include the **exact string** from the rule in the output JSON.
  - If no match is found, return an empty string for that rule.

#### **Resume Key**:
- Analyze the resume to find keywords, phrases, or contextual matches that semantically align with the job description.
- Provide a single aggregated list of matches from the resume.

#### **Job Metadata**:
- **job_location**: Extract the job location from the job description. If no location is mentioned, set the value to "Not Specified".
- **job_position**: Extract the job position or title from the job description. Provide this as a single string.

---

### **Format**:
```json
  "prolog": {{
    "Location": "Exact string from rule or empty string",
    "Compensation": "Exact string from rule or empty string",
    "Education Level": "Exact string from rule or empty string",
    "Pay": "Exact string from rule or empty string",
    "Skills": "Exact string from rule or empty string",
    "Tools": "Exact string from rule or empty string",
    "Certifications": "Exact string from rule or empty string",
    "Years of Experience": "Exact string from rule or empty string",
    "Number of Papers Published": "Exact string from rule or empty string",
    "Sponsorship": "Exact string from rule or empty string",
    "Work Authorization": "Exact string from rule or empty string"
  }},
  "resume": {{
    "matches": ["Item1", "Item2", "Item3", ...]
  }},
  "job_metadata": {{
    "job_location": "Job location from description or 'Not Specified'",
    "job_position": "Job position or title from description"
  }}
'''
**Job Description**:
{description}
**Prolog Rules**:
{user_rules}
**Resume**:
{resume_data}
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that extracts key information from job descriptions.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    content = response.choices[0].message.content.strip()
    json_content = clean_response(content)
    if json_content:
        try:
            extracted_info = json.loads(json_content)
            result = json.dumps(extracted_info)
            logger.info("Returning from OpenAI service")
            return result  # Re-serialize to ensure valid JSON
        except json.JSONDecodeError as e:
            logger.error(f"JSON decoding failed: {e}")
            logger.error(f"Content that caused the error: {json_content}")
            raise
    else:
        raise ValueError("Assistant's response did not contain valid JSON.")
"""
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

        prompt = f
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
"""