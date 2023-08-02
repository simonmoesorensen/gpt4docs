from autodocs import File
from autodocs import PyDefinition, PyDefinitionTypeEnum


def test_init(file):
    assert isinstance(file, File)
    assert file.file_path == "tests/data/test.py"
    assert isinstance(file.original_documentation, dict)
    assert isinstance(file.documentation, dict)


def test_scan_for_documentation(file):
    assert "test_func" in file.documentation
    assert "test_func2" in file.documentation
    assert "TestClass" in file.documentation
    assert "no_docstring" in file.documentation

    func1 = file.documentation["test_func"]
    assert isinstance(func1, PyDefinition)
    assert func1.type == "def"
    assert func1.docstring.strip() == '"""This is a test function"""'
    assert func1.docstring_start_line == 2
    assert func1.docstring_end_line == 2

    func2 = file.documentation["test_func2"]
    expected_docstring = '"""This is a test function\n\n    with multiple lines"""'
    assert func2.docstring.strip() == expected_docstring
    assert func2.type == "def"
    assert func2.docstring_start_line == 7
    assert func2.docstring_end_line == 9

    func3 = file.documentation["TestClass"]
    expected_docstring = (
        '"""This is a test class\n    with\n    other\n    syntax\n\n    """'
    )
    assert func3.docstring.strip() == expected_docstring
    assert func3.type == "class"
    assert func3.docstring_start_line == 15
    assert func3.docstring_end_line == 20

    func4 = file.documentation["no_docstring"]
    assert func4.docstring is None
    assert func4.type == "def"
    assert func4.docstring_start_line is None
    assert func4.docstring_end_line is None


def test_set_documentation(file):
    new_docstring = "This is a new docstring"
    file.set_documentation("test_func", new_docstring)
    assert file.documentation["test_func"].docstring == new_docstring


def test_replace_function_docstring(tmp_path):
    p = tmp_path / "test.py"
    p.write_text('def test_func():\n    """This is a test function"""\n    pass\n')
    file = File(str(p))

    new_doc = PyDefinition(
        type=PyDefinitionTypeEnum.function, name="test_func", docstring="New docstring"
    )
    new_content = file._write_docstring(p.read_text(), new_doc)

    expected_content = 'def test_func():\n    """New docstring"""\n    pass\n'
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

    expected_content = 'def test_func(arg1, arg2):\n    """New docstring"""\n    pass\n'
    assert new_content == expected_content


def test_replace_class_docstring(tmp_path):
    p = tmp_path / "test.py"
    p.write_text('class TestClass:\n    """This is a test class"""\n    pass\n')
    file = File(str(p))

    new_doc = PyDefinition(
        type=PyDefinitionTypeEnum.class_, name="TestClass", docstring="New docstring"
    )
    new_content = file._write_docstring(p.read_text(), new_doc)

    expected_content = 'class TestClass:\n    """New docstring"""\n    pass\n'
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
        'class TestClass(arg1, arg2):\n    """New docstring"""\n    pass\n'
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

    expected_content = 'def test_func():\n    """New docstring"""\n    pass\n'
    assert new_content == expected_content


def test_add_class_docstring(tmp_path):
    p = tmp_path / "test.py"
    p.write_text("class TestClass:\n    pass\n")
    file = File(str(p))

    new_doc = PyDefinition(
        type=PyDefinitionTypeEnum.class_, name="TestClass", docstring="New docstring"
    )
    new_content = file._write_docstring(p.read_text(), new_doc)

    expected_content = 'class TestClass:\n    """New docstring"""\n    pass\n'
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
    file.set_documentation("test_func", "New docstring\n    Its good")
    file.save()

    with p.open() as f:
        content = f.read()
    print(content)
    expected_content = 'def test_func():\n    """New docstring\n    Its good"""\n    print("hello world")\n    pass\n'  # noqa: E501
    assert content == expected_content


def test_get_docs(file):
    docs = file.get_docs()
    assert "test_func" in docs
    assert "test_func2" in docs
    assert "TestClass" in docs
    assert "no_docstring" in docs


def test_get_original_docs(file):
    original_docs = file.get_original_docs()
    assert "test_func" in original_docs
    assert "test_func2" in original_docs
    assert "TestClass" in original_docs
    assert "no_docstring" in original_docs


def test_str(file):
    assert isinstance(str(file), str)
