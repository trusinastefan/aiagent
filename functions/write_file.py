import os


def write_file(working_directory: str, file_path: str, content: str) -> str:

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        target_path_is_valid = os.path.commonpath([target_file, working_dir_abs]) == working_dir_abs
    
        if not target_path_is_valid:
            raise RuntimeError(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        
        if os.path.isdir(target_file):
            raise RuntimeError(f'Error: Cannot write to "{file_path}" as it is a directory')
        
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return (f'Error: Something went wrong!!!\n{e}')


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Creates a file on the specified path (relative to the working directory) and with the specified contents",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to a file that should be created, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "The contents of the created file",
                }
            },
            "required": ["file_path", "content"]
        },
    },
}
