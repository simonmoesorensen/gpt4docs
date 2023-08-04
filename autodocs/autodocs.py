"""Main module."""
from pathlib import Path
from autodocs import Project

project = Project(Path(__file__).parent)

# Index files with vectorstore
vectorstore = VectorStore()
vectorstore.index(project.files)

# Prompt LLM for docstring
llm = LLM()
for file in files:
    for definition in file.definitions:
        docstring = llm(file)
        definition.docstring = docstring

file.write()
