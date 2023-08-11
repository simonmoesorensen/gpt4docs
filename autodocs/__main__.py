import autodocs.logger_config  # noqa: F401
import asyncio
import time
from autodocs import ProjectManager, VectorStoreManager, LLMManager
from dotenv import load_dotenv
from pathlib import Path
import logging
import argparse

load_dotenv()
logger = logging.getLogger(__name__)


class MainApplication:
    def __init__(self, args):
        self._verify_args(args)

        if args.build:
            VectorStoreManager.build(args.vectorstore_path, args.project_path)

        self.project_manager = ProjectManager(args.project_path)
        self.vector_store_manager = VectorStoreManager(args.vectorstore_path)
        self.llm_manager = LLMManager(self.vector_store_manager.vectorstore)

    async def run(self):
        logger.info("Running")
        start = time.time()
        docstrings = await self.llm_manager.generate_docstrings(self.project_manager)
        self.project_manager.update_docstrings(docstrings)

        logger.info(f"Finished. Time spent: {time.time() - start:.2f}s")
        self.project_manager.save()

    def __call__(self, args: argparse.Namespace):
        if args.build:
            self.vector_store_manager.build(self.project_manager.project.project_root)
        else:
            asyncio.run(self.run())

    def _verify_args(self, args):
        if not args.project_path.exists():
            raise ValueError(f"Project path {args.project_path} does not exist")

        if not args.build and not VectorStoreManager.is_built(args.vectorstore_path):
            raise ValueError(
                "Vectorstore is not built. Run module with `--build` argument. "
                "`python3 -m autodocs --build ..."
            )

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "project_path",
            type=Path,
            help="Path to root of project to write documentation for",
        )
        parser.add_argument(
            "vectorstore_path",
            type=Path,
            default=Path.cwd() / ".vectorstore",
            nargs="?",
            help="Path to vectorstore directory",
        )
        parser.add_argument(
            "--build",
            action="store_true",
            help="Build vectorstore",
        )
        args = parser.parse_args()

        logger.info(f"Arguments: {args}")
        return args


if __name__ == "__main__":
    args = MainApplication.parse_args()
    app = MainApplication(args)
    asyncio.run(app.run())
