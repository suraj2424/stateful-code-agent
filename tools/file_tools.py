import os
import subprocess
from langchain.tools import tool

WORKING_DIR = "workspace"

@tool
def list_files_in_workspace():
    """Lists all files in the workspace directory."""
    files = []
    for root, _, filenames in os.walk(WORKING_DIR):
        for f in filenames:
            files.append(os.path.join(root, f))
    return "\n".join(files)

@tool
def read_file(file_path: str):
    """Reads the content of a specific file."""
    if not file_path.startswith(WORKING_DIR):
        file_path = os.path.join(WORKING_DIR, file_path)
    with open(file_path, 'r') as f:
        return f.read()

@tool
def write_file(file_path: str, content: str):
    """Writes content to a file."""
    if not file_path.startswith(WORKING_DIR):
        file_path = os.path.join(WORKING_DIR, file_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(content)
    return f"Successfully wrote to {file_path}"

@tool
def lint_code(file_path: str):
    """Checks for Python syntax errors."""
    if not file_path.startswith(WORKING_DIR):
        file_path = os.path.join(WORKING_DIR, file_path)
    try:
        with open(file_path, "r") as f:
            source = f.read()
        compile(source, file_path, 'exec')
        return "Syntax OK"
    except Exception as e:
        return f"Syntax Error: {str(e)}"

@tool
def execute_code(file_path: str):
    """Runs the python file and returns output or errors."""
    if not file_path.startswith(WORKING_DIR):
        file_path = os.path.join(WORKING_DIR, file_path)
    try:
        result = subprocess.run(["python", file_path], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return f"Success! Output:\n{result.stdout}"
        else:
            return f"Runtime Error:\n{result.stderr}"
    except Exception as e:
        return f"Execution failed: {str(e)}"

tools = [list_files_in_workspace, read_file, write_file, lint_code, execute_code]