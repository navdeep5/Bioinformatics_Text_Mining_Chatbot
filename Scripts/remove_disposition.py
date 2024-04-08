import json
from tqdm import tqdm

# Input and output file paths
input_file_path = 'Data/test_150_hard_coded_Karan.jsonl'
output_file_path = 'Data/test_150_hard_coded_Karan_fixed.jsonl'

# Process each line in the input JSONL file
with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', encoding='utf-8') as output_file:
    # Get the total number of lines in the input file
    total_lines = sum(1 for _ in input_file)
    input_file.seek(0)  # Reset file pointer to start
    
    # Iterate through each line and use tqdm to track progress
    for line in tqdm(input_file, total=total_lines, desc='Processing'):
        data = json.loads(line)
        input_text = data['input']
        
        # Replace <disposition>1</disposition> with just "1"
        modified_text = input_text.replace('<disposition>1</disposition>', '1')
        modified_text = modified_text.replace('disposition>1</disposition>', '1')

        # Update the 'input' field with the modified text
        data['input'] = modified_text
        
        # Write the modified data back to the output file
        output_file.write(json.dumps(data, ensure_ascii=False) + '\n')
