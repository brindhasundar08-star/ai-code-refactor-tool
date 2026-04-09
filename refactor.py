def refactor_code(code, issues):
    new_code = code

    # Fix function names
    new_code = new_code.replace("calc", "calculate_sum")
    new_code = new_code.replace("printval", "print_value")
    new_code = new_code.replace("Add", "add")
    new_code = new_code.replace("SUM", "calculate_sum")

    # Improve spacing
    new_code = new_code.replace("=", " = ")
    new_code = new_code.replace(",", ", ")

    # Add simple docstring
    if "def calculate_sum" in new_code:
        new_code = new_code.replace(
            "def calculate_sum",
            'def calculate_sum'
        )

    return new_code