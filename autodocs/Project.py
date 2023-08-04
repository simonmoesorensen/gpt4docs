from pathlib import Path
from autodocs import File
import logging

logger = logging.getLogger(__name__)


class Project:
    def __init__(self, project_root: str | Path):
        if isinstance(project_root, str):
            project_root = Path(project_root)

        self.project_root = project_root
        self.files = list(map(File, self.project_root.glob("**/*.py")))

    def save(self):
        for file in self.files:
            file.save()
        logger.info(f"Saved {len(self.files)} files")

    def _tree(self, dir_path: Path, padding: str = "", print_files: bool = True):
        """Represent the directory tree as a string."""
        # Tree based on https://stackoverflow.com/a/9728478/4416928
        if dir_path.is_dir():
            dirs = [d for d in dir_path.iterdir() if d.is_dir()]
            files = [f for f in dir_path.iterdir() if f.is_file()]
            if not dirs and not files:
                return f"{padding}└── {dir_path.name}/"
            if print_files:
                contents = [
                    *map(lambda d: self._tree(d, padding + "│   "), dirs),
                    *map(lambda f: f"{padding}│   ├── {f.name}", files),
                ]
            else:
                contents = [*map(lambda d: self._tree(d, padding + "│   "), dirs)]
            return "\n".join(
                [f"{padding}├── {dir_path.name}/", *contents, f"{padding}└──"]
            )
        else:
            return f"{padding}└── {dir_path.name}"

    def __str__(self) -> str:
        return self._tree(self.project_root, print_files=True)
