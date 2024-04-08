import json
from tqdm import tqdm
import os

# Path
input_dir = "Abstract_Generation"
output_dir = "Data"
output_name = "abstracts.jsonl"

# List of input filenames
input_files = []
for file in os.listdir(input_dir):
    input_files.append(os.path.join(input_dir, file))


# Output filename
output_file = os.path.join(output_dir, output_name)

# Function to combine JSONL files
def combine_jsonl_files(input_files, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for input_file in tqdm(input_files, desc="Combining files", unit=" file"):
            with open(input_file, 'r', encoding='utf-8', errors='ignore') as infile:
                for line in infile:
                    outfile.write(line)

# Call the function to combine files
combine_jsonl_files(input_files, output_file)

print(f"Combined files. Check '{output_file}' for the result.")
