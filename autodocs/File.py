import re
from typing import Dict
from pathlib import Path
from autodocs import PyDefinition
import logging

logger = logging.getLogger(__name__)


class File:
    """This class will scan a Python file and return all the functions
    and classes in it"""

    original_definitions: Dict[str, PyDefinition] = {}
    definitions: Dict[str, PyDefinition] = {}

    def __init__(self, file_path: str | Path) -> None:
        """Initializes the Scanner with the file path"""
        if isinstance(file_path, str):
            file_path = Path(file_path)

        # Regex for finding functions or classes, and docstrings
        self.re_definitions = r"""(?P<definition> *\b(?P<type>def|class)\b (?P<name>\w*) *\(?.*?\)?:)\n( *\"{3}(?P<docstring>[\s\S]*?)\"{3}\n?)?"""  # noqa: E501

        self.content = self._read_file(file_path)
        self.file_path = file_path

        self.original_definitions = self._scan_for_definitions()
        self.definitions = self.original_definitions

    def _read_file(self, file_path):
        with open(file_path, "r") as f:
            return f.read()

    def _scan_for_definitions(self) -> None:
        """Scans the file for functions and classes and their definitions"""

        defs = {}

        # Create definitions from all matches
        for match in re.finditer(self.re_definitions, self.content):
            defs[match.group("name")] = PyDefinition(
                type=match.group("type"),
                name=match.group("name"),
                docstring=match.group("docstring"),
            )
        return defs

    def _handle_indentation(self, match, definition) -> str:
        # Indentation level is 4 spaces + any spaces before the definition
        indentation_level = 4
        indentation_level += len(re.search(r"^ *", match.group("definition")).group(0))

        # Apply indentation to full docstring (with quotations)
        indented_docstring = []
        for line in definition.full_docstring.split("\n"):
            # Line is empty (no indentation)
            if line.strip() == "":
                # Important to add empty line to avoid unwanted whitespaces
                indented_docstring.append("")
                continue

            # Line is already indented
            if line.startswith(" " * indentation_level):
                indented_docstring.append(line)
                continue

            # Line is not indented, but not empty. Indent it.
            indented_docstring.append(" " * indentation_level + line)

        return "\n".join(indented_docstring)

    def _write_docstring(self, lines: str, definition: PyDefinition) -> str:
        """Find the definition in the file and write the docstring from the
        pydefinition object"""
        if definition.docstring is None:
            return lines

        # Regex to find specific definition
        re_definition = (
            rf"(?P<definition> *\b(?P<type>{definition.type})\b (?P<name>{definition.name}) *\(?.*?\)?:)\n"  # noqa: E501
            + r"( *\"{3}(?P<docstring>[\s\S]*?)\"{3}\n?)?"
        )

        # Match to find indentation level
        match = re.search(re_definition, lines)

        if match is None:
            logger.warning(
                f"Could not find definition {definition.name} in file {self.file_path}"
            )
            return lines

        indented_docstring = self._handle_indentation(match, definition)

        replacement = rf"\g<definition>\n{indented_docstring}\n"
        new_code = re.sub(re_definition, replacement, lines, flags=re.MULTILINE)

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
