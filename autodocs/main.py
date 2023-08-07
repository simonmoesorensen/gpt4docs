"""Main module."""
import autodocs.logger_config  # noqa: F401

from dotenv import load_dotenv
from pathlib import Path
from autodocs import LLM, Project
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from tqdm import tqdm

from autodocs.scripts.build_vectorstore import build_vectorstore

load_dotenv()


project = Project(Path(__file__).parent)
persist_directory = project.project_root.parent / "data" / ".chroma"


def run():
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
    llm = LLM(retriever=retriever, chain_type="stuff")

    for file in tqdm(
        project.files,
        desc="Iterating over files",
        position=0,
        leave=True,
    ):
        for definition in tqdm(
            file.get_docs(),
            desc="Iterating over definitions",
            position=1,
            leave=False,
        ):
            docstring = llm(definition.name)
            definition.docstring = docstring

    project.save()


if __name__ == "__main__":
    print("Running")
    run()
    print("Ran")
