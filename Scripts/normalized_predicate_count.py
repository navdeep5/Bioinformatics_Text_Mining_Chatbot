import jsonlines
import matplotlib.pyplot as plt
from collections import defaultdict

# Initialize a defaultdict to count occurrences of middle strings
middle_string_counts = defaultdict(int)

# Open the JSONL file and parse through it
with jsonlines.open('Triplets_replacement_unique/merged_normalized_unique_triplets.jsonl') as reader:
    for line in reader:
        middle_string = line[1]
        middle_string_counts[middle_string] += 1

# Define the desired order of categories
categories = ['causes', 'biolocation is', 'has role of', 'involved in', 'exposed through', 'sourced through']

# Sort the middle string counts based on the desired order of categories
sorted_counts = {category: middle_string_counts[category] for category in categories}

# Define colors for each bar
colors = ['skyblue', 'lightgreen', 'lightcoral', 'lightsalmon', 'lightseagreen', 'plum']

# Plotting the histogram
plt.figure(figsize=(10, 6))
plt.bar(sorted_counts.keys(), sorted_counts.values(), color=colors)
plt.xlabel('Predicates')
plt.ylabel('Count')
plt.title('Total Number of Triplets for Each Predicate')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Print the counts
for middle_string, count in sorted_counts.items():
    print(f'{middle_string}: {count}')
