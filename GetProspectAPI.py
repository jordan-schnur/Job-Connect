import os

import requests
import json

from dotenv import load_dotenv
from typing import Optional, List
from dataclasses import dataclass


def get_contact_info(linkedin_url):
    url = "https://api.getprospect.com/public/v1/insights/contact"

    load_dotenv()

    api_key = os.getenv("GET_PROSPECT_API_KEY")
    headers = {
        'X-API-Key': api_key
    }
    params = {
        'linkedinUrl': linkedin_url,
        'apiKey': api_key
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return "Error: " + str(response.status_code)


@dataclass
class LinkedInContact:
    first_name: str
    last_name: str
    contact_info: Optional[str]
    summary: str
    company: 'Company'
    linkedin: List['LinkedInID']
    geolocation: str
    last_updated_at: Optional[str]
    email: Optional[str]
    get_prospect_id: str


@dataclass
class Company:
    name: str
    domain: str
    position: str


@dataclass
class LinkedInID:
    id: str
    type: str


def response_to_linkedin_contact(response_json: dict) -> LinkedInContact:
    company_info = Company(**response_json['company'])
    linkedin_ids = [LinkedInID(**li) for li in response_json['linkedin']]
    return LinkedInContact(
        first_name=response_json['firstName'],
        last_name=response_json['lastName'],
        contact_info=response_json.get('contactInfo'),
        summary=response_json['summary'],
        company=company_info,
        linkedin=linkedin_ids,
        geolocation=response_json['geolocation'],
        last_updated_at=response_json.get('lastUpdatedAt'),
        email=response_json.get('email'),
        get_prospect_id=response_json['getProspectId']
    )
