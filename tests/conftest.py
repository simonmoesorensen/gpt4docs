import pytest
from autodocs import File


@pytest.fixture
def file():
    return File("tests/data/test.py")
