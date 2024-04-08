import json
import matplotlib.pyplot as plt
from tqdm import tqdm
from collections import Counter

# Read the JSONL file
compound_cluster = 'clustered_triplet_data.jsonl'
random_cluster = 'Triplets_replacement_unique/randomly_sampled_triplets.jsonl'
strict_cluster = 'Clusters/strict_correlated_clusters.jsonl'
with open(strict_cluster, 'r') as file:
    lines = file.readlines()

# Extract the number of items in each line
item_counts = []

# Use tqdm to add a progress bar
for line in tqdm(lines, desc="Processing lines", unit="line"):
    data = json.loads(line)
    item_counts.append(len(data) - 1)  # Subtracting 1 as you mentioned in the comments

# Generate a histogram
plt.hist(item_counts, bins=range(min(item_counts), min(200, max(item_counts) + 2)), align='left', edgecolor='black')
plt.xlabel('Number of Triplets per Line')
plt.ylabel('Frequency')
plt.title('Distribution of Number of Triplers per Line')
# plt.xlim(0, 100)  # Set x-axis limit between 0 and 200
plt.grid(True)
plt.show()
