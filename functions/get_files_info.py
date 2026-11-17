import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    
    contents = []
    error_str = None
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        target_path_is_valid = os.path.commonpath([target_dir, working_dir_abs]) == working_dir_abs
    
        if not target_path_is_valid:
            raise RuntimeError(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    
        if not os.path.isdir(target_dir):
            raise RuntimeError(f'Error: "{directory}" is not a directory')
    except Exception as e:
        error_str = (f'Error: Something went wrong!!!\n{e}')
    
    if target_path_is_valid:
        try:
            for item in os.listdir(target_dir):
                item_path = os.path.join(target_dir, item)
                item_size = os.path.getsize(item_path)
                item_name = os.path.basename(item_path)
                item_is_dir = os.path.isdir(item_path)
                contents.append(f'- {item_name}: file_size={item_size} bytes, is_dir={item_is_dir}')
        except Exception as e:
            error_str = (f'Error: An error occured while iterating over the items of the target directory!!!\n{e}')

    
    return f'Result for \'{directory}\' directory:\n' +  (error_str if error_str is not None else '\n'.join(contents))


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
