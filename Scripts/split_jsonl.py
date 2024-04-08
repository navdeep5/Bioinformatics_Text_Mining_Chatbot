import json
import os

def divide_jsonl(input_file, output_prefix, k):
    with open(input_file, 'r') as f:
        jsonl_content = f.readlines()

    total_lines = len(jsonl_content)
    lines_per_file = total_lines // k

    if lines_per_file == 0:
        print(f"The number of lines in the JSONL file is less than {k}. Cannot divide equally.")
        return

    for i in range(k):
        start_index = i * lines_per_file
        end_index = (i + 1) * lines_per_file

        output_file = f"{output_prefix}_{i+1}.jsonl"
        with open(output_file, 'w') as f:
            f.writelines(jsonl_content[start_index:end_index])

        print(f"Created {output_file} with {lines_per_file} lines.")

# Replace 'input.jsonl' and 'output_prefix' with your file names
# Replace 'k' with the number of files you want to create
divide_jsonl('Clusters/correlated_random_clsuters.jsonl', 'Parsed_Correlated_Clusters/correlated_cluster_parse', 6)
