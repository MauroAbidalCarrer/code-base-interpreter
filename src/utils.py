import openai
import os
import re
import ast

def generate_unique_filename(filename, directory_path):
    """
    This function takes a file name and a directory path, checks for existing files in the directory that contain the file name,
    and returns a unique file name with an incremented number before the file extension if necessary.
    """
    # Check if the file already exists in the directory
    full_path = os.path.join(directory_path, filename)
    if not os.path.exists(full_path):
        return full_path
    
    # Split the filename into name and extension
    name, extension = os.path.splitext(filename)
    
    # Initialize the maximum found number to 1 (since we start numbering from 2)
    max_num = 1
    
    # Regular expression to match files with a number appended
    pattern = re.compile(re.escape(name) + r"_(\d+)" + re.escape(extension))
    
    # Find all files in the directory and determine the highest number used
    for file in os.listdir(directory_path):
        if file == filename:
            max_num = max(max_num, 1)
        else:
            match = pattern.match(file)
            if match:
                # Extract the number and update max_num if it's higher than the current max_num
                num = int(match.group(1))
                max_num = max(max_num, num)
    
    # Generate the new filename with the incremented number
    new_filename = f"{name}_{max_num + 1}{extension}"
    return os.path.join(directory_path, new_filename)

def extract_classes_and_functions(file_path):
    """
    Extracts classes and standalone functions from a given Python file.

    Args:
    file_path (str): The path to the Python file.

    Returns:
    tuple: A tuple containing two lists, one for classes and one for functions.
    """

    with open(file_path, "r") as file:
        source = file.read()
        node = ast.parse(source)

    classes = [n.name for n in node.body if isinstance(n, ast.ClassDef)]
    functions = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]

    # Extracting the main code (code not inside a class or function)
    main_code = []
    for n in node.body:
        if not isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            start_line, start_column = n.lineno, n.col_offset
            end_line, end_column = getattr(n, "end_lineno", start_line), getattr(n, "end_col_offset", start_column)
            main_code_lines = source.splitlines()[start_line-1:end_line]
            main_code_lines[-1] = main_code_lines[-1][:end_column]
            main_code.append("\n".join(main_code_lines))

    main_code_content = "\n".join(main_code)

    return classes, functions, main_code_content

def setup_opena_AI_key():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key is None:
        openai_api_key = input("Please enter your OpenAI API key.")
    openai.api_key = openai_api_key     

if __name__ == "__main__":
    import sys
    classes, functions, main_code_content = extract_classes_and_functions(sys.argv[1])
    print("classes:", classes)
    print("functions:", functions)
    print("main_code_content:", main_code_content)
