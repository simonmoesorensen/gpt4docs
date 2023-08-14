import pytest
from gpt4docs import File, Project
from pathlib import Path
import os

TEST_DATA = Path("tests/data/")


@pytest.fixture
def file():
    return File(TEST_DATA / "test.py")


@pytest.fixture
def project_root():
    return TEST_DATA / "test_package"


@pytest.fixture
def project(project_root):
    return Project(project_root)


# Clean up all files after each test
@pytest.fixture(autouse=True)
def teardown():
    # Run test
    yield

    # Remove all directories with "_my_suffix" suffix recursively
    new_dirs = TEST_DATA.rglob("*_my_suffix")
    for dir_ in new_dirs:
        os.system(f"rm -rf {dir_}")
