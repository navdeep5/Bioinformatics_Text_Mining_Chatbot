import json
import random
from collections import defaultdict
from tqdm import tqdm

def load_data(input_file):
    data = []
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line))
    return data

def select_triplet(grouped_data, linked_entities, predicate_counters):
    if linked_entities:
        selected_predicate = min(predicate_counters, key=predicate_counters.get)
        valid_triplets = [triplet for triplet in grouped_data[selected_predicate] if any(entity in linked_entities for entity in triplet[:2])]
    else:
        selected_predicate = random.choice(list(grouped_data.keys()))
        valid_triplets = grouped_data[selected_predicate]
    # print("Valid triplets:", valid_triplets)  # Debugging statement
    if not valid_triplets:
        print("No valid triplets found for predicate:", selected_predicate)  # Debugging statement
    selected_triplet = random.choice(valid_triplets)
    predicate_counters[selected_predicate] += 1
    return selected_triplet



def create_output_lines(grouped_data, total_lines):
    output_lines = []
    predicate_counters = {predicate: 0 for predicate in grouped_data.keys()}
    with tqdm(total=total_lines, desc="Creating output lines") as pbar:
        while len(output_lines) < total_lines:
            line_length = random.randint(3, 5)
            line_triplets = []
            linked_entities = set()
            while len(line_triplets) < line_length:
                triplet = select_triplet(grouped_data, linked_entities, predicate_counters)
                line_triplets.append(triplet)
                linked_entities.update(triplet[:2])
            output_lines.append(line_triplets)
            pbar.update(1)
    return output_lines

def write_output(output_file, output_lines):
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in output_lines:
            file.write(json.dumps(line) + '\n')

def main(input_file, output_file, total_lines):
    data = load_data(input_file)
    grouped_data = defaultdict(list)
    for triplet in data:
        predicate = triplet[1]
        grouped_data[predicate].append(triplet)
    output_lines = create_output_lines(grouped_data, total_lines)
    write_output(output_file, output_lines)

if __name__ == "__main__":
    input_file = "Triplets_replacement_unique/merged_normalized_unique_triplets.jsonl"
    output_file = "Clusters/strict_correlated_clusters.jsonl"
    total_lines = 2500
    main(input_file, output_file, total_lines)
