import json
import os

def count_lines_in_jsonl_files(file_paths):
    total_lines = 0

    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            total_lines += len(lines)
            print(f"{file_path.split(os.sep)[-1]}: {len(lines)}")

    return total_lines

# Replace 'path/to/your/files' with the actual path where your JSONL files are located
directory_path = 'Triplets'

# Get a list of all JSONL files in the specified directory
jsonl_files = [file for file in os.listdir(directory_path) if file.endswith('.jsonl')]

# Construct the full file paths
file_paths = [os.path.join(directory_path, file) for file in jsonl_files]

# Count the total number of lines in the JSONL files
total_lines = count_lines_in_jsonl_files(file_paths)

print(f'Total number of lines in JSONL files: {total_lines}')
