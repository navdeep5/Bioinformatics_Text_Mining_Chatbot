import json
import re

with open('Evaluation/Manual_Evaluation/Mixtral_Transformer_Finetuned/Mixtral_Transformer_Finetuned_Sentence_Tagged/output_80_sentence_tags_NoOE.jsonl', 'r', encoding='utf-8') as file:
    lines = file.readlines()

count = 0

for i, line in enumerate(lines):
    data = json.loads(line)
    if not data['output']:
        count += 1
        data['output_complete'] = data['output_complete'].replace('\u201d', '"').replace('\u201c', '"')
        pattern = r'\["([^"]+)",\s*"([^"]+)",\s*"([^"]+)"\]'
        triplets = re.findall(pattern, data['output_complete'])
        triplets = [triple for triple in triplets if 'NA' not in triple and "unknown" not in triple]
        data['output'] = triplets
        lines[i] = json.dumps(data)
    
    cleaned_list = []
    for triple in data['output']:
        triple = [s.replace('\\"', '"') for s in triple]
        if 'NA' in triple or 'unknown' in triple:
            continue
        
        # Check if sublist is ['subject', 'predicate', 'object']
        if triple == ['subject', 'predicate', 'object']:
            continue
        
        cleaned_list.append(triple)
    data['output'] = cleaned_list
    lines[i] = json.dumps(data)


with open('Evaluation/Manual_Evaluation/Mixtral_Transformer_Finetuned/Mixtral_Transformer_Finetuned_Sentence_Tagged/output_80_sentence_tags_NoOE_Fixed.jsonl', 'w', encoding='utf-8') as file:
    for line in lines:
        line = line.strip()  # Remove leading and trailing whitespace
        if line:  # Check if line is not empty after stripping
            file.write(line + '\n')  # Add newline character after each line


print(count)