import os

# Specify the directory you want to list the files of
directory = 'source_code/gpt-4-turbo-research'

""" list all the .py files in the parent directory and child directories """
files_and_directories = [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory) for f in filenames]

""" filter the files_and_directories for .py files """


def get_py_files():
    py_files = [f for f in files_and_directories if f.endswith('.py')]
    return py_files


""" load the content of a file by name """


def load_file_by_name(file_name):
    with open(f"{file_name}", "r") as file:
        return file.read()
