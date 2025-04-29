import os
import sys
from pathlib import Path

# Check error
def validate_file_path(file_path):
    trimmed_path = file_path.strip()

    if not trimmed_path:
        print("Error: The file path is empty.", file=sys.stderr)
        return False

    path_obj = Path(trimmed_path)

    if not path_obj.exists():
        print(f"Error: The file at {trimmed_path} does not exist.", file=sys.stderr)
        return False
    elif not path_obj.is_file():
        print(f"Error: The path at {trimmed_path} is not a valid file.", file=sys.stderr)
        return False

    return True

# Read file
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            for line_number, line in enumerate(f, start=1):
                print(f"Line {line_number}: {line.rstrip()}")
    except Exception as e:
        print(f"Error: Could not open the file {file_path}\n{e}", file=sys.stderr)

# Main function
def main():
    try:
        file_path = input("Enter file path: ").strip()
    except EOFError:
        print("No input provided.", file=sys.stderr)
        return

    if not validate_file_path(file_path):
        return

    read_file(file_path)

if __name__ == "__main__":
    main()
