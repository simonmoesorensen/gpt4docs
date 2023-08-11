"""Main module."""
import autodocs.logger_config  # noqa: F401

import asyncio
import time
from dotenv import load_dotenv
from pathlib import Path
from autodocs import LLM, Project
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

from autodocs.scripts.build_vectorstore import build_vectorstore

load_dotenv()


project = Project(Path(__file__).parent)
persist_directory = project.project_root.parent / "data" / ".chroma"


def setup():
    build_vectorstore(
        persist_directory=persist_directory,
        documents_folder=project.project_root,
    )

    # Index files with vectorstore
    vectorstore = Chroma(
        collection_name="documents",
        persist_directory=str(persist_directory),
        embedding_function=OpenAIEmbeddings(),
    )
    retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 6})

    # Prompt LLM for docstring
    llm = LLM(model_name="gpt-3.5-turbo-16k", retriever=retriever)
    return llm


async def run(llm):
    for file in project.files.values():
        print(f"File: {file.file_path}")

        tasks = [llm.arun(definition.name) for definition in file.get_docs()]
        docstrings = await asyncio.gather(*tasks)

        for definition, docstring in zip(file.get_docs(), docstrings):
            file.set_docstring(definition.name, docstring)

    project.save()


if __name__ == "__main__":
    print("Running")
    llm = setup()
    start = time.time()
    asyncio.run(run(llm))
    print("Finished")
    print(f"Time taken: {time.time() - start}")
