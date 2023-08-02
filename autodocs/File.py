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
        self.content = self._read_file(file_path)
        self.file_path = file_path

        self.original_documentation = self._scan_for_documentation()
        self.documentation = self.original_documentation

    def _read_file(self, file_path):
        with open(file_path, "r") as f:
            return f.read()

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

    def _write_docstring(self, lines: str, definition: PyDefinition) -> str:
        """Find the definition in the file and write the docstring from the
        pydefinition object"""

        # Pattern to match when docstring exists
        pattern_existing_doc = (
            rf"(?P<definition>{definition.type} {definition.name}.*?:)\n"
            rf"\s*\"\"\"(?P<existing_doc>.*?)\"\"\"\n"
        )
        # Pattern to match when no docstring exists
        pattern_no_doc = rf"(?P<definition>{definition.type} {definition.name}.*?:)\n"

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

        with open(self.file_path, "w") as f:
            f.writelines(lines)

    def get_docs(self) -> Dict[str, PyDefinition]:
        return self.documentation

    def get_original_docs(self) -> Dict[str, PyDefinition]:
        return self.original_documentation

    def __str__(self) -> str:
        return str(self.documentation)
