import re
from typing import Dict
from pathlib import Path
from autodocs import PyDefinition


class File:
    """This class will scan a Python file and return all the functions
    and classes in it"""

    original_definitions: Dict[str, PyDefinition] = {}
    definitions: Dict[str, PyDefinition] = {}

    def __init__(self, file_path: str | Path) -> None:
        """Initializes the Scanner with the file path"""
        if isinstance(file_path, str):
            file_path = Path(file_path)

        self.content = self._read_file(file_path)
        self.file_path = file_path

        self.original_definitions = self._scan_for_definitions()
        self.definitions = self.original_definitions

    def _read_file(self, file_path):
        with open(file_path, "r") as f:
            return f.read()

    def _scan_for_definitions(self) -> None:
        """Scans the file for functions and classes and their definitions"""
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
            rf"(?P<definition>^\s*{definition.type} {definition.name}\(?.*?\)?:)\n"
            rf"\s*\"\"\"(?P<existing_doc>[\s\S]*?)\"\"\"\n"
        )
        # Pattern to match when no docstring exists
        pattern_no_doc = (
            rf"(?P<definition>^\s*{definition.type} {definition.name}\(?.*?\(?:)\n"
        )

        # Match to find indentation level
        match = re.search(pattern_existing_doc, lines) or re.search(
            pattern_no_doc, lines
        )

        if match is None:
            return lines

        # Indentation level is 4 spaces + any spaces before the definition
        indentation_level = 4
        indentation_level += len(re.search(r"^\s*", match.group("definition")).group(0))

        # Apply indentation to full docstring (with quotations)
        indented_docstring = "\n".join(
            " " * indentation_level + line if line else line
            for line in definition.full_docstring.split("\n")
        )

        if re.search(pattern_existing_doc, lines, flags=re.DOTALL):
            replacement = rf"\g<definition>\n{indented_docstring}\n"
            new_code = re.sub(pattern_existing_doc, replacement, lines, flags=re.DOTALL)
        else:
            replacement = rf"\g<definition>\n{indented_docstring}\n"
            new_code = re.sub(pattern_no_doc, replacement, lines)

        return new_code

    def set_docstring(self, name: str, docstring: str) -> None:
        """Set the definitions for a given function or class in the file"""
        self.definitions[name].docstring = docstring

    def save(self, path: Path = None, overwrite: bool = False) -> None:
        """Writes the new definitions to the file"""
        lines = self.content

        for definition in self.definitions.values():
            lines = self._write_docstring(lines, definition)

        if overwrite:
            path = self.file_path
        elif path is None:
            raise ValueError("Path must be specified if overwrite is False")

        with open(path, "w") as f:
            f.writelines(lines)

    def get_docs(self) -> Dict[str, PyDefinition]:
        return self.definitions.values()

    def get_original_docs(self) -> Dict[str, PyDefinition]:
        return self.original_definitions

    def __str__(self) -> str:
        return str(self.definitions)
