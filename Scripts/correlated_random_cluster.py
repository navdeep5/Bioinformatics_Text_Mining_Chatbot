import json
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def find_related_lines(data, target):
    related_lines = []
    for line in data:
        if line[0] == target or line[2] == target:
            related_lines.append(line)
    return related_lines

def process_iteration(data):
    # Randomly pick a line (X)
    random_line = random.choice(data)

    # Find lines that contain either the first or last element of X
    related_lines = find_related_lines(data, random_line[0]) + find_related_lines(data, random_line[2])

    # Randomly select 2 to 5 lines from the related lines
    num_related_lines = random.randint(2, 5)
    selected_related_lines = random.sample(related_lines, min(num_related_lines, len(related_lines)))

    # Include X in the new list and add the selected related lines
    new_list = [random_line] + selected_related_lines

    return new_list

def generate_new_jsonl(input_file, output_file, k):
    with open(input_file, 'r') as infile:
        data = [json.loads(line) for line in infile]

    new_data = []

    with ThreadPoolExecutor() as executor, tqdm(total=k, desc='Processing') as pbar:
        futures = [executor.submit(process_iteration, data) for _ in range(k)]

        for future in as_completed(futures):
            new_list = future.result()
            new_data.append(new_list)
            pbar.update(1)

    # Write the new data to the output JSONL file
    with open(output_file, 'w') as outfile:
        for item in new_data:
            json.dump(item, outfile)
            outfile.write('\n')

# Example usage
generate_new_jsonl('Triplets_replacement_unique/merged_triplets.jsonl', 'correlated_random_clsuters.jsonl', 3000)
