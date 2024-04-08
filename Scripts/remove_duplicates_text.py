import json
import argparse
import re
from tqdm import tqdm
import ast

# Function to remove duplicate lines
def remove_duplicates(input_file, output_file):
    unique_lines = set()

    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

        for line in tqdm(lines):
            # Add the JSON-formatted line to the set of unique lines
            unique_lines.add(line)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Write the unique lines to the output file
        for unique_line in unique_lines:
            outfile.write(str(unique_line))

    print(f"New file contains {len(unique_lines)} lines.")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Required parameters
    parser.add_argument(
        "--input_file", default=None, type=str, required=True, help="Input JsonL."
    )

    parser.add_argument(
        "--output_file", default=None, type=str, required=True, help="Output JsonL."
    )

    args = parser.parse_args()

    # Call the function to remove duplicates
    remove_duplicates(args.input_file, args.output_file)

    print(f"Duplicate removal completed. Check {args.output_file} for the result.")
