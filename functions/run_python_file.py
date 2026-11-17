import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    
    try:

        working_dir_abs = os.path.abspath(working_directory)
        file_abs = os.path.abspath(os.path.join(working_dir_abs, file_path))
        file_path_is_valid = os.path.commonpath([working_dir_abs, file_abs]) == working_dir_abs

        if not file_path_is_valid:
            raise RuntimeError(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        
        if not os.path.isfile(file_abs):
            raise RuntimeError(f'Error: "{file_path}" does not exist or is not a regular file')
        
        if os.path.splitext(file_path)[1] != '.py':
            raise RuntimeError(f'Error: "{file_path}" is not a Python file')
        
        command = ["python", file_abs]
        if args:
            command.extend(args)
        result = subprocess.run(command, capture_output=True, cwd=working_directory, timeout=30, text=True)
        result_returncode = result.returncode
        result_stdout = result.stdout
        result_stderr = result.stderr
        result_str = ''
        if result_returncode != 0:
            result_str += f'Process exited with code {result_returncode}'
        if not result_stdout and not result_stderr:
            result_str += f'No output produced'
        else:
            result_str += f'STDOUT: {result_stdout}'
            result_str += f'STDERR: {result_stderr}'
    
    except Exception as e:
        result_str = f'Error: executing Python file: {e}'
    
    return result_str


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run the python file with the specified path (relative to the working directory)",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the python file that should be executed, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "The command line arguments passed to the python script",
                }
            },
            "required": ["file_path"]
        },
    },
}
