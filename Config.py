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


#   "technologies": [
#     "WordPress",
#     "PHP",
#     "JavaScript",
#     "React",
#     "Angular",
#     "Git",
#     "HTML",
#     "CSS"
#   ]


@dataclass
class Configuration:
    user: User = None
    emailTemplate: EmailTemplate = None
    technologies: list[str] = None

    def __init__(self):
        with open("config.json", "r") as stream:
            try:
                data = json.load(stream)
                self.user = User(**data['user'])
                self.emailTemplate = EmailTemplate(**data['emailTemplate'])
                self.technologies = data['technologies']  # Directly as a list
            except json.JSONDecodeError as e:
                print(f"Error reading config: {e}")
                raise e
