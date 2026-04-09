import ast

def test_code(old_code, new_code):
    """
    Validate that old_code and new_code are syntactically valid Python sources.

    Returns True if both parse successfully, otherwise False.
    """
    try:
        ast.parse(old_code)
        ast.parse(new_code)
        return True
    except SyntaxError:
        return False
    except TypeError:
        return False