import json
import random

def copy_random_records(input_file, output_file, num_records):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = f.readlines()

    # Shuffle the data to randomize the selection
    random.shuffle(data)

    # Select a random subset of records
    selected_data = data[:num_records]

    # Write the selected records to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(selected_data)

# Example usage:
input_file = "Abstract_Generation/gpt_abstract.jsonl"
output_file = "Data/gpt_mixtral_train.jsonl"
num_records = 2000  # Specify the number of random records to copy

copy_random_records(input_file, output_file, num_records)
