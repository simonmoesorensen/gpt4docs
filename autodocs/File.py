import re
from typing import Dict
from pathlib import Path
from autodocs import PyDefinition


class File:
    """This class will scan a Python file and return all the functions
    and classes in it"""

    original_documentation: Dict[str, PyDefinition] = {}
    documentation: Dict[str, PyDefinition] = {}

    def __init__(self, file_path: str | Path) -> None:
        """Initializes the Scanner with the file path"""
        if isinstance(file_path, str):
            file_path = Path(file_path)

        self.content = self._read_file(file_path)
        self.file_path = file_path

        self.original_documentation = self._scan_for_documentation()
        self.documentation = self.original_documentation

    def _read_file(self, file_path):
        with open(file_path, "r") as f:
            return f.read()

    def _scan_for_documentation(self) -> None:
        """Scans the file for functions and classes and their documentation"""
        # Regex for finding functions or classes, and docstrings
        re_definitions = r"""(?P<definition>\S?\b(?P<type>def|class)\b (?P<name>\w*) *\(?.*?\)?:)\n\s*(\"{3}(?P<docstring>[\s\S]*?)\"{3}\n?)?"""  # noqa: E501

        defs = {}

        # Create definitions from all matches
        for match in re.finditer(re_definitions, self.content):
            defs[match.group("name")] = PyDefinition(
                type=match.group("type"),
                name=match.group("name"),
                docstring=match.group("docstring"),
            )
        return defs

    def _write_docstring(self, lines: str, definition: PyDefinition) -> str:
        """Find the definition in the file and write the docstring from the
        pydefinition object"""
        if definition.docstring is None:
            return lines

        # Pattern to match when docstring exists
        pattern_existing_doc = (
            rf"(?P<definition>{definition.type} {definition.name}\(?.*?\)?:)\n"
            rf"\s*\"\"\"(?P<existing_doc>[\s\S]*?)\"\"\"\n"
        )
        # Pattern to match when no docstring exists
        pattern_no_doc = (
            rf"(?P<definition>{definition.type} {definition.name}\(?.*?\(?:)\n"
        )

        if re.search(pattern_existing_doc, lines, flags=re.DOTALL):
            replacement = rf'\g<definition>\n    """{definition.docstring}"""\n'
            new_code = re.sub(pattern_existing_doc, replacement, lines, flags=re.DOTALL)
        else:
            replacement = rf'\g<definition>\n    """{definition.docstring}"""\n'
            new_code = re.sub(pattern_no_doc, replacement, lines)

        return new_code

    def set_documentation(self, name: str, docstring: str) -> None:
        """Set the documentation for a given function or class in the file"""
        self.documentation[name].docstring = docstring

    def save(self, overwrite: bool = False) -> None:
        """Writes the new documentation to the file"""
        lines = self.content

        for definition in self.documentation.values():
            lines = self._write_docstring(lines, definition)

        if overwrite:
            file_path = self.file_path
        else:
            # Add .new to the file name
            file_path = self.file_path.parent / (
                self.file_path.name.removesuffix(".py") + ".new.py"
            )

        with open(file_path, "w") as f:
            f.writelines(lines)

    def get_docs(self) -> Dict[str, PyDefinition]:
        return self.documentation.values()

    def get_original_docs(self) -> Dict[str, PyDefinition]:
        return self.original_documentation

    def __str__(self) -> str:
        return str(self.documentation)
