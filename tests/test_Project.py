from autodocs import File, PyDefinition, PyDefinitionTypeEnum, Project
from pathlib import Path


def test_project_init(project_root):
    project = Project(project_root)
    assert isinstance(project.project_root, Path)
    assert project.project_root == project_root


def test_project_files(project):
    files = list(project.files.values())
    assert len(files) == 8
    assert isinstance(files[0], File)


def test_project_save(tmp_path, project):
    new_doc = PyDefinition(
        type=PyDefinitionTypeEnum.function, name="test_func", docstring="New docstring"
    )
    file = project.files["func1.py"]
    file.set_docstring("test_func", new_doc.docstring)
    project.save(suffix="_my_suffix")

    new_root = project.project_root.parent / (project.project_root.name + "_my_suffix")
    assert new_root.exists()
    assert new_root.name == "test_package_my_suffix"

    # Verify that the file has been placed in the new directory with a new docstring
    p = new_root / file.file_path.relative_to(project.project_root)

    with p.open() as f:
        content = f.read()

    with project.files["func1_formatted.py"].file_path.open() as f:
        expected_content = f.read()

    assert content == expected_content

    # Verify that all files have been placed in the new directory
    for file in project.files.values():
        path = new_root / file.file_path.relative_to(project.project_root)
        assert path.exists()


def test_project_tree(project):
    expected_str = """├── test_package/
│   ├── nested_package/
│   │   ├── test.py
│   └──
│   ├── func1.py
│   ├── terminal.py
│   ├── func1_formatted.py
│   ├── time_manager.py
│   ├── weather_manager.py
│   ├── main.py
│   ├── package1.py
└──"""
    assert str(project) == expected_str
