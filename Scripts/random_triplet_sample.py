import json
import random
from tqdm import tqdm

# Read the input file
input_file_path = 'Triplets_replacement_unique/merged_triplets.jsonl'
with open(input_file_path, 'r') as infile:
    data = [json.loads(line) for line in infile]

# Output file path
output_file_path = 'Triplets_replacement_unique/randomly_sampled_triplets.jsonl'

# Total lines you want in the output file
total_lines = 50000

# Open the output file and write lines
with open(output_file_path, 'w') as outfile:
    for _ in tqdm(range(total_lines)):
        # Randomly sample x (between 2 and 10) lists
        x = random.randint(2, 10)
        sampled_lists = random.sample(data, x)
        
        # Write the line to the output file
        outfile.write(json.dumps(sampled_lists) + '\n')