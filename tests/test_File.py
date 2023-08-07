from autodocs import File
from autodocs import PyDefinition, PyDefinitionTypeEnum
from pathlib import Path


def test_init(file):
    assert isinstance(file, File)
    assert file.file_path == Path("tests/data/test.py")
    assert isinstance(file.original_definitions, dict)
    assert isinstance(file.definitions, dict)


def test_scan_for_definitions(file):
    assert "test_func" in file.definitions
    assert "test_func2" in file.definitions
    assert "TestClass" in file.definitions
    assert "no_docstring" in file.definitions

    func1 = file.definitions["test_func"]
    assert isinstance(func1, PyDefinition)
    assert func1.type == "def"
    assert func1.docstring == "This is a test function"

    func2 = file.definitions["test_func2"]
    expected_docstring = "This is a test function\n\n    with multiple lines"
    assert func2.docstring == expected_docstring
    assert func2.type == "def"

    func3 = file.definitions["TestClass"]
    expected_docstring = "This is a test class\n    with\n    other\n    syntax\n\n    "
    assert func3.docstring == expected_docstring
    assert func3.type == "class"

    func4 = file.definitions["no_docstring"]
    assert func4.docstring is None
    assert func4.type == "def"


def test_set_docstring(file):
    new_docstring = "This is a new docstring"
    file.set_docstring("test_func", new_docstring)
    assert file.definitions["test_func"].docstring == new_docstring


def test_replace_function_docstring(tmp_path):
    p = tmp_path / "test.py"
    p.write_text('def test_func():\n    """This is a test function"""\n    pass\n')
    file = File(str(p))

    new_doc = PyDefinition(
        type=PyDefinitionTypeEnum.function, name="test_func", docstring="New docstring"
    )
    new_content = file._write_docstring(p.read_text(), new_doc)

    expected_content = (
        'def test_func():\n    """\n    New docstring\n    """\n    pass\n'
    )
    assert new_content == expected_content


def test_replace_function_with_args_docstring(tmp_path):
    p = tmp_path / "test.py"
    p.write_text(
        'def test_func(arg1, arg2):\n    """This is a test function"""\n    pass\n'
    )
    file = File(str(p))

    new_doc = PyDefinition(
        type=PyDefinitionTypeEnum.function, name="test_func", docstring="New docstring"
    )
    new_content = file._write_docstring(p.read_text(), new_doc)

    expected_content = (
        'def test_func(arg1, arg2):\n    """\n    New docstring\n    """\n    pass\n'
    )
    assert new_content == expected_content


def test_replace_class_docstring(tmp_path):
    p = tmp_path / "test.py"
    p.write_text('class TestClass:\n    """This is a test class"""\n    pass\n')
    file = File(str(p))

    new_doc = PyDefinition(
        type=PyDefinitionTypeEnum.class_, name="TestClass", docstring="New docstring"
    )
    new_content = file._write_docstring(p.read_text(), new_doc)

    expected_content = (
        'class TestClass:\n    """\n    New docstring\n    """\n    pass\n'
    )
    assert new_content == expected_content


def test_replace_class_with_args_docstring(tmp_path):
    p = tmp_path / "test.py"
    p.write_text(
        'class TestClass(arg1, arg2):\n    """This is a test class"""\n    pass\n'
    )
    file = File(str(p))

    new_doc = PyDefinition(
        type=PyDefinitionTypeEnum.class_, name="TestClass", docstring="New docstring"
    )
    new_content = file._write_docstring(p.read_text(), new_doc)

    expected_content = (
        'class TestClass(arg1, arg2):\n    """\n    New docstring\n    """\n    pass\n'
    )
    assert new_content == expected_content


def test_add_function_docstring(tmp_path):
    p = tmp_path / "test.py"
    p.write_text("def test_func():\n    pass\n")
    file = File(str(p))

    new_doc = PyDefinition(
        type=PyDefinitionTypeEnum.function, name="test_func", docstring="New docstring"
    )
    new_content = file._write_docstring(p.read_text(), new_doc)

    expected_content = (
        'def test_func():\n    """\n    New docstring\n    """\n    pass\n'
    )
    assert new_content == expected_content


def test_add_class_docstring(tmp_path):
    p = tmp_path / "test.py"
    p.write_text("class TestClass:\n    pass\n")
    file = File(str(p))

    new_doc = PyDefinition(
        type=PyDefinitionTypeEnum.class_, name="TestClass", docstring="New docstring"
    )
    new_content = file._write_docstring(p.read_text(), new_doc)

    expected_content = (
        'class TestClass:\n    """\n    New docstring\n    """\n    pass\n'
    )
    assert new_content == expected_content


def test_save(file, tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "test.py"
    p.write_text(
        'def test_func():\n    """This is a test function"""\n    print("hello world")\n    pass\n'  # noqa
    )

    file = File(str(p))
    print(file.content)
    file.set_docstring("test_func", "New docstring\n    Its good")

    # Save in new dir
    new_dir = tmp_path / "sub_new"
    new_dir.mkdir()
    p = new_dir / "test.py"

    file.save(path=p)

    # Verify new path
    with p.open() as f:
        content = f.read()

    expected_content = 'def test_func():\n    """\n    New docstring\n    Its good\n    """\n    print("hello world")\n    pass\n'  # noqa: E501
    assert content == expected_content
    assert (tmp_path / "sub" / "test.py").exists() and (
        tmp_path / "sub_new" / "test.py"
    ).exists()


def test_get_docs(file):
    docs = file.get_docs()
    assert len(docs) == 4


def test_get_original_docs(file):
    original_docs = file.get_original_docs()
    assert "test_func" in original_docs
    assert "test_func2" in original_docs
    assert "TestClass" in original_docs
    assert "no_docstring" in original_docs


def test_str(file):
    assert isinstance(str(file), str)


def test_indentation_level_preserved_double_indent(tmp_path):
    p = tmp_path / "test.py"
    p.write_text(
        '    def test_func(arg1, arg2):\n        """This is a test function"""\n        pass\n'  # noqa
    )
    file = File(str(p))

    new_docstring = "New line 1\nNew line 2"
    new_doc = PyDefinition(
        type=PyDefinitionTypeEnum.function, name="test_func", docstring=new_docstring
    )
    new_content = file._write_docstring(p.read_text(), new_doc)

    # Notice how the new docstring lines are indented with 4 spaces
    expected_content = (
        '    def test_func(arg1, arg2):\n        """\n        New line 1\n'
        '        New line 2\n        """\n        pass\n'
    )
    assert new_content == expected_content


def test_indentation_level_preserved(tmp_path):
    p = tmp_path / "test.py"
    p.write_text(
        'def test_func(arg1, arg2):\n    """This is a test function"""\n    pass\n'
    )
    file = File(str(p))

    new_docstring = "New line 1\nNew line 2"
    new_doc = PyDefinition(
        type=PyDefinitionTypeEnum.function, name="test_func", docstring=new_docstring
    )
    new_content = file._write_docstring(p.read_text(), new_doc)

    # Notice how the new docstring lines are indented with 4 spaces
    expected_content = (
        'def test_func(arg1, arg2):\n    """\n    New line 1\n'
        '    New line 2\n    """\n    pass\n'
    )
    assert new_content == expected_content
