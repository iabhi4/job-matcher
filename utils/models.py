from pydantic import BaseModel
from typing import List

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

categories = [
    "Location",
    "Experience Level",
    "Programming Languages",
    "Technology Stacks",
    "Tools and Software",
    "Cloud Platforms",
    "Industries",
    "Company Size",
    "Salary Range",
    "Work Authorization",
    "Job Type",
    "Remote Work Preference",
    "Education Level",
    "Certifications",
    "Language Proficiency",
    "Work Schedule",
    "Travel Requirements",
    "Company Culture",
    "Benefits",
    "Preferred Technologies"
]