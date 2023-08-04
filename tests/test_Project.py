from autodocs import File, PyDefinition, PyDefinitionTypeEnum, Project
from pathlib import Path


def test_project_init(project_root):
    project = Project(project_root)
    assert isinstance(project.project_root, Path)
    assert project.project_root == project_root


def test_project_files(project):
    files = list(project.files)
    assert len(files) == 2
    assert isinstance(files[0], File)


def test_project_save(tmp_path, project):
    new_doc = PyDefinition(
        type=PyDefinitionTypeEnum.function, name="test_func", docstring="New docstring"
    )
    file = project.files[0]
    file.set_documentation("test_func", new_doc.docstring)
    project.save()

    p = file.file_path.parent / file.file_path.name.replace(".py", ".new.py")
    print(p)
    with p.open() as f:
        content = f.read()

    with file.file_path.open() as f:
        expected_content = f.read().replace(
            """\"\"\"This is a test function\"\"\"""", """\"\"\"New docstring\"\"\""""
        )

    assert content == expected_content


def test_project_tree(project):
    expected_str = """├── test_package/
│   ├── func1.py
│   ├── package1.py
└──"""
    assert str(project) == expected_str
