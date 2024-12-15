# Job Matcher

## Overview

This is a tool I created for my class project CPSC-583 to analyze job descriptions and match it with your resume and some rules that you have created to see how well your profile matches with the job description. There is still a lot to be done to make this a reliable tool like optimizing the LLM prompt, improving the scoring logic and adding auth.

## Workflow

### User Setup:
User inputs personal details and uploads a resume.
The resume is parsed, and key details are extracted.

### Rule Creation:
Users define rules based on their preferences (e.g., location, skills).

### Job Matching:
GPT analyzes the job description to extract relevant data.
Prolog matches the extracted information with user-defined rules.
A match score and detailed analysis are generated.

### Dashboard:
Users view matched jobs with detailed analysis.
New job descriptions can be analyzed via the dashboard.

## Installation and Setup

To set up and run the Job Matcher on your local machine, follow these steps:

1. Clone the repository:
   `git clone https://github.com/iabhi4/job-matcher.git`

2. Create a virtual environment and activate it
   `python -m venv venv`
   `source venv/bin/activate`
3. Install dependencies:
   `pip install -r requirements.txt`

4. Configure environment variable in a .env file in the root directory of the project
   `MONGO_URI=<your-mongodb-uri>`
   `OPENAI_API_KEY=<your-openai-api-key>`

5. Start the backend server
   `uvicorn main:app --reload --port 8080`

6. Install the frontend dependencies and start the frontend
   `npm install`
   `npm run dev`

Feel free to dive into the project, test the functionalities, and push improvements or bug fixes. If you encounter any issues or have suggestions, don't hesitate to contact or contribute directly to the repo.

---
