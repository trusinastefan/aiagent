import os

from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    file_content_string = ''
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        target_path_is_valid = os.path.commonpath([target_file, working_dir_abs]) == working_dir_abs
    
        if not target_path_is_valid:
            raise RuntimeError(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    
        if not os.path.isfile(target_file):
            raise RuntimeError(f'Error: File not found or is not a regular file: "{file_path}"')
        
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

    except Exception as e:
        file_content_string = (f'Error: Something went wrong!!!\n{e}')
    
    return file_content_string

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Returns contents of a file with the specified path (relative to the working directory)",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to a file, whose contents should be returned, relative to the working directory (default is the working directory itself)",
                },
            },
            "required": ["file_path"]
        },
    },
}
