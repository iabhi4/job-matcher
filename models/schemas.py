from pydantic import BaseModel
from typing import List, Optional

class Rule(BaseModel):
    category: str
    rule: str

class RuleSet(BaseModel):
    user_id: str
    rules: List[Rule]

class PersonalDetails(BaseModel):
    name: str
    email: str
    phone: str
    linkedin: str
    github: str

class Experience(BaseModel):
    company: str
    role: str
    location: str
    startDate: str
    endDate: str
    responsibilities: str

class Project(BaseModel):
    name: str
    description: str
    technologies: str
    startDate: str
    endDate: str

class Skills(BaseModel):
    languages: str
    frameworks: str
    developerTools: str
    libraries: str

class Education(BaseModel):
    institution: str
    degree: str
    location: str
    startYear: str
    endYear: str

class Resume(BaseModel):
    personalDetails: PersonalDetails
    experience: List[Experience]
    projects: List[Project]
    skills: Skills
    education: List[Education]

class User(BaseModel):
    name: str
    resume: Resume

class Job(BaseModel):
    userId: str
    companyName: str
    jobTitle: str
    location: str
    matchScore: int
    companyLogo: Optional[str]
    detailedAnalysis: Optional[dict] = None  # To store the prolog and resume analysis details


rules = """
{
  "user_id": "unique_user_id",
  "rules": [
    {"category": "Skills", "rule": "Python"},
    {"category": "Location", "rule": "Remote"}
  ]
}
"""

jobs = """
{
  "userId": "unique_user_id",
  "companyName": "Tech Corp",
  "jobTitle": "Software Engineer",
  "location": "Remote",
  "matchScore": 85,
  "companyLogo": null,
  "detailedAnalysis": {
    "matching_score": 85,
    "matched_rules": ["Skills: Python", "Location: Remote"]
  }
}
"""