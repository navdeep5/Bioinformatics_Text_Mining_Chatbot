import json
import argparse
import re
from tqdm import tqdm

# Function to remove duplicate lines
def remove_duplicates(input_file, output_file):
    unique_lines = set()

    with open(input_file, 'r') as infile:
        lines = infile.readlines()

        for line in tqdm(lines):
            # Convert each line to a JSON list
            data = json.loads(line)
            # Convert the list back to a JSON-formatted string
            json_line = json.dumps(data)

            # Add the JSON-formatted line to the set of unique lines
            unique_lines.add(json_line)

    with open(output_file, 'w') as outfile:
        # Write the unique lines to the output file
        for unique_line in unique_lines:
            outfile.write(unique_line + '\n')

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
