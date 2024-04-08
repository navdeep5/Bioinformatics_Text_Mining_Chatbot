import json

# Input and output file paths
input_file_path = "Data/train_data.jsonl"
output_file_path = "Data/ner_train_data.jsonl"

# Read data from JSONL file
data = []
with open(input_file_path, "r", encoding="utf-8") as file:
    for line in file:
        data.append(json.loads(line))

# Process data and convert "output" lists to dictionaries
for entry in data:
    output = []
    for item in entry["output"]:
        output_dict = {
            "chemical": item[0],
            "predicate": item[1],
            "object": item[2]
        }
        output.append(output_dict)
    entry["output"] = output

# Write processed data to a new JSONL file
with open(output_file_path, "w") as file:
    for entry in data:
        file.write(json.dumps(entry) + "\n")
