import json
from collections import Counter
import matplotlib.pyplot as plt
from tqdm import tqdm

# Initialize a counter to store the occurrences of each middle string
middle_string_counter = Counter()

# Path to your JSONL file
jsonl_file_path = 'Abstract_Generation/gpt_abstract.jsonl'

# Get the total number of lines in the file for tqdm
total_lines = sum(1 for line in open(jsonl_file_path))

# Read each line of the JSONL file
with open(jsonl_file_path, 'r') as file:
    for line in tqdm(file, total=total_lines, desc="Processing JSONL"):
        # Parse JSON data from the line
        data = json.loads(line)
        outputs = data['output']

        # Iterate over each output sublist
        for sublist in outputs:
            # Get the middle string from the sublist
            middle_string = sublist[1]
            # Increment the counter for this middle string
            middle_string_counter[middle_string] += 1

# Create lists of middle strings and their corresponding counts for plotting
middle_strings = list(middle_string_counter.keys())
counts = list(middle_string_counter.values())

# Plot the histogram
plt.figure(figsize=(10, 6))
plt.barh(middle_strings, counts, color='skyblue')
plt.xlabel('Occurrences')
plt.ylabel('Predicates')
plt.title('Histogram of Predicate Occurrences')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.savefig(f"Histograms/test_data_150_equal.png")
plt.show()