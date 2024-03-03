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
class Configuration:
    user: User = None

    def __init__(self):
        with open("config.json", "r") as stream:
            try:
                data = json.load(stream)
                self.user = User(**data['user'])
            except json.JSONDecodeError as e:
                print(f"Error reading config: {e}")
                raise e
