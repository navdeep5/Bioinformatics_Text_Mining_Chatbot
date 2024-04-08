import json
import matplotlib.pyplot as plt
from tqdm import tqdm

# Input and output filenames
input_file = 'Triplets_replacement_unique/merged_triplets.jsonl'
output_file = 'clustered_triplet_data.jsonl'

# Function to cluster the data, save it to a JSONL file, and generate a histogram
def cluster_save_and_plot(input_file, output_file):
    clustered_data = {}

    with open(input_file, 'r') as infile:
        lines = infile.readlines()
        for line in tqdm(lines, desc="Clustering", unit=" lines"):
            data = json.loads(line)
            compound_name = data[0]

            if compound_name not in clustered_data:
                clustered_data[compound_name] = []

            triplet = data
            clustered_data[compound_name].append(triplet)

    # Save the clustered data to a JSONL file
    with open(output_file, 'w') as outfile:
        for compound_name, triplets in tqdm(clustered_data.items(), desc="Writing to JSONL", unit=" compounds"):
            # json.dump([compound_name] + triplets, outfile)
            json.dump(triplets, outfile)
            outfile.write('\n')

    print(f"Clustered data saved to '{output_file}'.")

# Call the function to cluster the data, save it to a JSONL file, and generate a histogram
cluster_save_and_plot(input_file, output_file)