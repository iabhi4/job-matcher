from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_db():
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["job-matcher"]
    return db


resume_schema = {
  "personalDetails": {
    "name": "string",
    "email": "string",
    "phone": "string",
    "linkedin": "string",
    "github": "string"
  },
  "experience": [
    {
      "company": "string",
      "role": "string",
      "location": "string",
      "startDate": "string",
      "endDate": "string",
      "responsibilities": "string"
    }
  ],
  "projects": [
    {
      "name": "string",
      "description": "string",
      "technologies": "string",
      "startDate": "string",
      "endDate": "string"
    }
  ],
  "skills": {
    "languages": "string",
    "frameworks": "string",
    "developerTools": "string",
    "libraries": "string"
  },
  "education": [
    {
      "institution": "string",
      "degree": "string",
      "location": "string",
      "startYear": "string",
      "endYear": "string"
    }
  ]
}