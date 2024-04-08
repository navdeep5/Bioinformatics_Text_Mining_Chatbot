import json
import random
from tqdm import tqdm
import os

# Paths
input_file = os.path.join("Data", "abstracts.jsonl")

# Error count
error_count = 0

# Load the data from your existing JSONL file
with open(input_file, 'r', encoding='utf-8') as file:
    # Count the total number of lines for tqdm progress tracking
    total_lines = sum(1 for _ in file)

# Initialize tqdm with the total number of lines
with open(input_file, 'r', encoding='utf-8') as file:
    data = []
    for line in tqdm(file, total=total_lines, desc="Loading data", unit=" lines"):
        # Preprocess the line to replace single quotes with double quotes
        line = line.replace("'", "\"")        

        try:
            # Load the line as a JSON object
            json_object = json.loads(line)
            data.append(json_object)
        except json.JSONDecodeError as e:
            error_count += 1
            print(f"Error decoding JSON on line: {line.strip()}")
            print(f"Error details: {e}")

# Set the random seed for reproducibility
random.seed(42)

# Shuffle the data randomly
random.shuffle(data)

# Define the split ratio
split_ratio = 0.8  # 80% for training, 20% for testing

# Calculate the split index
split_index = int(len(data) * split_ratio)

# Split the data into training and test sets
train_data = data[:split_index]
test_data = data[split_index:]

# Write the training data to a new JSONL file
with open('train_data.jsonl', 'w', encoding='utf-8') as train_file:
    for item in tqdm(train_data, desc="Writing training data", unit=" items"):
        train_file.write(json.dumps(item) + '\n')

# Write the test data to a new JSONL file
with open('test_data.jsonl', 'w', encoding='utf-8') as test_file:
    for item in tqdm(test_data, desc="Writing test data", unit=" items"):
        test_file.write(json.dumps(item) + '\n')

print("Data split and new JSONL files created: train_data.jsonl and test_data.jsonl.")
print(f"Total number of error: {error_count}")
