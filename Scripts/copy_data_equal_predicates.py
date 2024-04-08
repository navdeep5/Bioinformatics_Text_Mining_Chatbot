import json
import random
from collections import Counter
from tqdm import tqdm

# Function to count the occurrences of middle strings in a JSONL file
def count_middle_strings(jsonl_file):
    middle_string_counter = Counter()
    with open(jsonl_file, 'r') as file:
        for line in file:
            data = json.loads(line)
            outputs = data['output']
            for sublist in outputs:
                middle_string = sublist[1]
                middle_string_counter[middle_string] += 1
    return middle_string_counter

# Function to select 150 lines from the JSONL file with roughly the same number of middle strings
def select_lines(jsonl_file, target_middle_strings, num_lines=150):
    selected_lines = []
    with open(jsonl_file, 'r') as file:
        for line in tqdm(file, desc="Selecting lines"):
            data = json.loads(line)
            outputs = data['output']
            # Count the number of middle strings in this line
            line_middle_strings = [sublist[1] for sublist in outputs]
            line_middle_string_counter = Counter(line_middle_strings)
            # Check if the line has roughly the same number of target middle strings
            selected_lines.append((line, line_middle_string_counter))
    
    # Randomly shuffle the lines to avoid bias
    random.shuffle(selected_lines)
    
    # Sort the lines by the difference between actual and target count of middle strings
    selected_lines.sort(key=lambda x: sum(abs(x[1][middle_string] - target_count) for middle_string, target_count in target_middle_strings.items()))
    
    # Select the top num_lines lines
    selected_lines = selected_lines[:num_lines]
    
    # Extract the lines without the counter
    selected_lines = [line for line, _ in selected_lines]
    
    return selected_lines

# Input and output file paths
input_jsonl_file = 'Data/test_data.jsonl'
output_jsonl_file = 'Data/test_150_equal.jsonl'

# Count the occurrences of middle strings in the input JSONL file
input_middle_strings = count_middle_strings(input_jsonl_file)
print("Middle strings counts in input JSONL file:", input_middle_strings)

# Calculate the target count for each middle string in the selected lines
target_middle_strings = {middle_string: sum(input_middle_strings.values()) // len(input_middle_strings) for middle_string in input_middle_strings}

# Select 150 lines from the input JSONL file with roughly the same number of middle strings overall
selected_lines = select_lines(input_jsonl_file, target_middle_strings)

# Write the selected lines to the output JSONL file
with open(output_jsonl_file, 'w') as file:
    file.writelines(selected_lines)

print("150 lines with roughly the same number of middle strings overall copied to", output_jsonl_file)
