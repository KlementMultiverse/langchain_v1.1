"""
Resume Data Models using Pydantic v2

Defines the structure for resume data extraction.
Each model represents a component of a resume.

Author: Klement
Date: December 15, 2025
"""



from pydantic import BaseModel,Field
from typing import List,Optional

class ContactInfo(BaseModel):
	""" Contact information- REQUIRED to reach the candidate( USA candidates only) """
	name: str = Field(description="Full name of the person")
	email: str = Field(description="Email Address ( required for contact)")
	phone: str = Field(description="Phone number as 10 digits only, no dashes or spaces (e.g., '5551234567'). Extract from formats like '555-123-4567', '(555) 123-4567', '+1-555-123-4567 ext.123' - keep only the 10 digits, remove country code, extensions, and formatting")
	location: Optional[str] = Field(default=None, description="City name only, without state or country (e.g., 'Austin' not 'Austin, TX')")

class JobExperience(BaseModel):
	"""Single job/work experience entry"""
	company: str = Field(description="Company or organization name")
	title: str = Field(description="Job title or position held")
	duration: str = Field(description="Time period (e.g., '2021-Present', 'Jan 2019 - Dec 2020', '2018-2020')")
	responsibilities: List[str] = Field(default_factory=list,description="List of key responsibilities, achievements, or bullet points from this job")


class Education(BaseModel):
	"""Single education entry (degree, certification, etc.)"""
	institution: str = Field(description="School, university, or institution name")
	degree: str = Field(description="Degree or certification name (e.g., 'Bachelor of Science', 'MBA', 'Master of Science')")
	field: Optional[str] = Field(default=None, description="Field of study or major (e.g., 'Computer Science', 'Business Administration')")
	year: Optional[str] = Field(default=None, description="Graduation year or time period (e.g., '2019', '2017-2021')")


class Resume(BaseModel):
	"""Complete resume structure - combines all components"""
	contact: ContactInfo = Field(description="Contact information to reach the candidate")
	summary: Optional[str] = Field(default=None,description="Professional summary or objective statement from the resume")
	skills: List[str] = Field(default_factory=list,description="List of skills, technologies, tools, or competencies mentioned in the resume")
	experience: List[JobExperience] = Field(default_factory=list,description="List of work experience entries, ordered from most recent to oldest")
	education: List[Education] = Field(default_factory=list,description="List of education entries (degrees, certifications, courses)")
