from src.utils import camel_to_snake


def test_single_word():
    assert camel_to_snake("hello") == "hello"


def test_single_uppercase_word():
    assert camel_to_snake("Hello") == "hello"


def test_camel_case():
    assert camel_to_snake("myVariableName") == "my_variable_name"


def test_single_uppercase_start():
    assert camel_to_snake("VariableName") == "variable_name"
