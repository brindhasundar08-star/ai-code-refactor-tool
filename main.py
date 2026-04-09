from analyzer import analyze_code
from refactor import refactor_code
from tester import test_code

def main():
    with open("legacy_code.py", "r", encoding="utf-8") as f:
        code = f.read()

    print("Analyzing...")
    issues = analyze_code(code)
    print("Issues:", issues)

    print("Refactoring...")
    new_code = refactor_code(code, issues)

    print("Testing...")
    if test_code(code, new_code):
        print("Success!\n")
        print(new_code)
    else:
        print("Failed! Rollback")


if __name__ == "__main__":
    main()