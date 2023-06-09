import re
from typing import Dict

from autodocs import PyDefinition


class File:
    """This class will scan a Python file and return all the functions
    and classes in it"""

    original_documentation: Dict[str, PyDefinition] = {}
    documentation: Dict[str, PyDefinition] = {}

    def __init__(self, file_path: str) -> None:
        """Initializes the Scanner with the file path"""
        self.file_path = file_path
        self.original_documentation = self._scan_for_documentation()
        self.documentation = self.original_documentation

    def _scan_for_documentation(self) -> None:
        """Scans the file for functions and classes and their documentation"""
        with open(self.file_path, "r") as f:
            lines = f.readlines()

        # Regex for finding functions or classes, and docstrings
        def_line_re = re.compile(r"^\s*(def|class)\s+(\w+)\b")
        docstring_start_re = re.compile(r'^\s*"""')
        docstring_end_re = re.compile(r'.*"""[\n?]$')

        # Loop through the lines and find the functions and classes
        defs = {}
        i = 0
        while i < len(lines):
            line = lines[i]
            match = def_line_re.match(line)
            if match:
                docstring = None
                docstring_start_line = None
                docstring_end_line = None

                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if docstring_start_re.match(next_line):
                        docstring_lines = []
                        i += 1

                        docstring_start_line = i + 1
                        while i < len(lines) and not docstring_end_re.match(lines[i]):
                            docstring_lines.append(lines[i])
                            i += 1
                        if i < len(lines) and docstring_end_re.match(lines[i]):
                            docstring_lines.append(lines[i])
                        docstring = "".join(docstring_lines).strip()
                        docstring_end_line = i + 1

                name = match.group(2)
                defs[name] = PyDefinition(
                    type=match.group(1),
                    name=name,
                    docstring_start_line=docstring_start_line,
                    docstring_end_line=docstring_end_line,
                    docstring=docstring,
                )
            i += 1

        return defs

    def _insert_docstring(self, line: str, docstring: str) -> str:
        """Inserts the docstring into the line"""
        return line.replace(":", f':\n"""{docstring}"""', 1)

    def _replace_docstring(self, line: str, docstring: str) -> str:
        """Replaces the docstring in the line"""
        return line.replace('"""', f'"""{docstring}', 1)

    def replace_documentation(self, name: str, docstring: str) -> None:
        """Replaces the documentation for a given function or class in the file"""
        self.documentation[name].docstring = docstring

    def write(self, overwrite: bool = False) -> None:
        """Writes the new documentation to the file"""
        with open(self.file_path, "r") as f:
            lines = f.readlines()

        for name, definition in self.documentation.items():
            if overwrite:
                lines[definition.line - 1] = self._replace_docstring(
                    lines[definition.line - 1], definition.docstring
                )
            else:
                lines[definition.line - 1] = self._insert_docstring(
                    lines[definition.line - 1], definition.docstring
                )

        with open(self.file_path, "w") as f:
            f.writelines(lines)

    def get_docs(self) -> Dict[str, PyDefinition]:
        return self.documentation

    def get_original_docs(self) -> Dict[str, PyDefinition]:
        return self.original_documentation

    def __str__(self) -> str:
        return str(self.documentation)
