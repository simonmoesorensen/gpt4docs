from autodocs.model import LLM
import asyncio
import logging

from autodocs.modules.managers.ProjectManager import ProjectManager

logger = logging.getLogger(__name__)


class LLMManager:
    def __init__(self, retriever):
        self.llm = LLM(model_name="gpt-3.5-turbo-16k", retriever=retriever)

    async def generate_docstrings(self, project_manager: ProjectManager):
        all_docstrings = {}

        for file in project_manager.get_files():
            logger.info(f"Generating docstrings in file: {file.file_path}")
            tasks = [
                self._generate_docstring(definition) for definition in file.get_docs()
            ]
            docstrings = await asyncio.gather(*tasks)
            all_docstrings.update({file.file_path: docstrings})

        logger.info("Finished generating docstrings")
        return all_docstrings

    async def _generate_docstring(self, definition):
        return {definition.name: await self.llm.arun(definition.name)}
