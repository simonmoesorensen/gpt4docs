from autodocs.modules.directory import Project
from typing import Dict
from pathlib import Path


class ProjectManager:
    def __init__(self, project_path: str):
        self.project = Project(Path(project_path))

    def update_docstrings(self, all_docstrings: Dict[str, Dict]):
        for file_path, file_docstrings in all_docstrings.items():
            print(file_docstrings)
            for def_name, docstring in file_docstrings.items():
                self.project.files[file_path].set_docstring(def_name, docstring)

    def save(self):
        self.project.save()

    def get_files(self):
        return self.project.files.values()
