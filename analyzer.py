def analyze_code(code):
    issues = []

    if "def calc" in code:
        issues.append("Bad function name: calc")

    if "def printval" in code:
        issues.append("Bad function name: printval")

    if "def Add" in code or "def SUM" in code:
        issues.append("Non-pythonic function naming")

    if "=" in code and " " not in code:
        issues.append("Poor spacing")

    if "  " not in code:
        issues.append("Formatting issue")

    return issues
