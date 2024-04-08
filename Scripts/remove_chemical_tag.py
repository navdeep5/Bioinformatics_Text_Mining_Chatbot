import json

def remove_chemical_tags(input_text):
    return input_text.replace("<CHEMICAL>", "").replace("</CHEMICAL>", "")

def process_file(input_file, output_file):
    with open(input_file, 'r', encoding="utf-8") as infile, open(output_file, 'w', encoding="utf-8") as outfile:
        for line in infile:
            data = json.loads(line)
            data['input'] = remove_chemical_tags(data['input'])
            data['output'] = [[remove_chemical_tags(triplet) for triplet in output_triplet] for output_triplet in data['output']]
            json.dump(data, outfile)
            outfile.write('\n')

input_file_path = 'Data/Tagging_Ground_Truth.jsonl'
output_file_path = 'Data/Tagging_Ground_Truth_No_Chemical.jsonl'
process_file(input_file_path, output_file_path)
