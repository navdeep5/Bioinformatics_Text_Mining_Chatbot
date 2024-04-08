import jsonlines
import os

def process_jsonl_files(directory):
    ids = set()
    output_set = set()

    # Iterate through each JSONL file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.jsonl'):
            file_path = os.path.join(directory, filename)
            with jsonlines.open(file_path) as reader:
                for obj in reader:
                    # Extract ids
                    if 'id' in obj:
                        ids.add(obj['id'])

                    # Extract output sublists
                    if 'output' in obj:
                        for sublist in obj['output']:
                            output_set.add(tuple(sublist))

    return ids, output_set

# Directory containing the JSONL files
jsonl_directory = 'Triplet_Extraction/Groq_Triplet_Extraction/Triple_Output5'

# Process JSONL files
ids, output_set = process_jsonl_files(jsonl_directory)

# Print the lengths of sets
print("Total unique IDs:", len(ids))
print("Total unique output sublists:", len(output_set))
