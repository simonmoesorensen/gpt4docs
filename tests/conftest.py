import pytest
from autodocs import File, Project
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


# Clean up all files after test
def pytest_sessionfinish(session, exitstatus):
    # Remove all .new.py files
    new_files = TEST_DATA.rglob("*.new.py")

    for file in new_files:
        os.remove(file)
