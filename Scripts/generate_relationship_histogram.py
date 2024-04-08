import json
from tqdm import tqdm
import matplotlib.pyplot as plt
import os

# Path to the JSONL file
input_file = os.path.join("Data", "abstracts.jsonl")

# Count errors
error_count = 0

# List to store extracted middle values
middle_values = []

# Count the total number of lines for tqdm progress tracking
total_lines = sum(1 for _ in open(input_file, 'r', encoding='utf-8'))

# Read and extract data from the JSONL file using tqdm
with open(input_file, 'r', encoding='utf-8', errors='ignore') as file:
    for line in tqdm(file, total=total_lines, desc="Processing JSONL", unit=" lines"):
        try:
            # Load the line as a JSON object
            line = line.replace("'", "\"").replace('"', '\"')
            # line = line.replace("'", '')


            # if 'Title: "' in line:
            #     line = line.replace('Title: "', 'Title: ').replace('"', "'")

            # if '"\n' in line:
            #     line = line.replace('"\n', '\n').replace('"', "'")

            json_object = json.loads(line)
            
            # Extract middle values from the "output" list
            middle_values.extend([item[1] for item in json_object['output']])
            
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON on line: {line.strip()}")
            print(f"Error details: {e}")
            error_count += 1

# List total error
print(f"Total errors: {error_count}")

# Create a histogram
plt.figure(figsize=(10, 6))
plt.hist(middle_values, bins=len(set(middle_values)), edgecolor='black', alpha=0.7)
plt.title('Frequency of Middle Values in "output" List')
plt.xlabel('Middle Values')
plt.ylabel('Frequency')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility

# Show the plot
plt.show()
