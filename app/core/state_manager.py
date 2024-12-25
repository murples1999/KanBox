#state_manager.py

import json
from app.models.project import Project

class StateManager:
    def __init__(self, save_file="kanbox_data.json"):
        self.projects = []
        self.last_open_project = None
        self.save_file = save_file

    def add_project(self, project):
        self.projects.append(project)

    def remove_project(self, project_name):
        self.projects = [p for p in self.projects if p.name != project_name]

    def save(self):
        try:
            with open(self.save_file, 'w') as f:
                json.dump(self.to_dict(), f, indent=4)
        except Exception as e:
            print(f"StateManager: Error saving state: {e}")

    def load(self):
        try:
            with open(self.save_file, 'r') as f:
                data = json.load(f)
                self.from_dict(data)
        except FileNotFoundError:
            print("StateManager: No save file found. Starting with an empty state.")
        except Exception as e:
            print(f"StateManager: Error loading state: {e}")

    def to_dict(self):
        return {
            "projects": [project.to_dict() for project in self.projects],
            "last_open_project": self.last_open_project,
        }

    def from_dict(self, data):
        self.projects = [Project.from_dict(p) for p in data.get("projects", [])]
        self.last_open_project = data.get("last_open_project")