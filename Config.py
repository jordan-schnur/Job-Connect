import json
from dataclasses import dataclass


@dataclass
class User:
    name: str
    email: str

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email


@dataclass
class EmailTemplate:
    subject: str
    body: str


@dataclass
class Configuration:
    user: User = None
    emailTemplate: EmailTemplate = None
    technologies: list[str] = None
    fuzzy_confidence: float = 80.0

    def __init__(self):
        with open("config.json", "r") as stream:
            try:
                data = json.load(stream)
                self.user = User(**data['user'])
                self.emailTemplate = EmailTemplate(**data['emailTemplate'])
                self.technologies = data['technologies']  # Directly as a list
                self.fuzzy_confidence = data['fuzzy_confidence']
            except json.JSONDecodeError as e:
                print(f"Error reading config: {e}")
                raise e
