from autodocs.modules.directory import Project
from typing import Dict
from pathlib import Path


class ProjectManager:
    def __init__(self, project_path: str):
        self.project = Project(Path(project_path))

    def update_docstrings(self, all_docstrings: Dict[str, Dict]):
        for file_path, definitions in all_docstrings.items():
            for def_ in definitions:
                self.project.files[str(file_path.name)].set_definition(def_)

    def save(self):
        self.project.save()

    def get_files(self):
        return self.project.files.values()
