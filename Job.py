from typing import Optional

from Recruiter import Recruiter


class Job:
    id = None
    title = None
    company_name = None
    location = None
    company_url = None
    description = None
    recruiter: Optional[Recruiter] = None

    def __init__(self, job_id, title, company_name, company_url, location, description, recruiter=None):
        self.id = job_id
        self.title = title
        self.company_name = company_name
        self.company_url = company_url
        self.location = location
        self.recruiter = recruiter
        self.description = description
