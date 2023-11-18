import os

# Define function to remove JSON files recursively
def remove_json_files(path):
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            if file.endswith('.json'):
                os.remove(os.path.join(dirpath, file))
                # print(os.path.join(dirpath, file))

# Call function to remove JSON files under current working directory
remove_json_files(os.getcwd())
