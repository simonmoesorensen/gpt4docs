def test_func():
    """This is a test function"""
    pass


def test_func2():
    """This is a test function

    with multiple lines"""
    a = 2
    return a


class TestClass:
    """This is a test class
    with
    other
    syntax

    """

    # Method with no docstring
    def no_docstring(self, x) -> None:
        return x**2
