import os
import re

def tag_words_with_category(categories_folder, input_text, priority_order):
    # Initialize an empty dictionary to store categories and their associated words
    categories = {}

    # Process each file in the categories folder
    for filename in os.scandir(categories_folder):
        if filename.name.endswith('.txt') and filename.is_file() and filename != "chemical.txt":
            category = os.path.splitext(filename.name)[0]  # Extract category name from filename
            with open(filename.path, 'r', encoding='utf-8') as file:
                words = {line.strip() for line in file if line.strip()}  # Read lines and remove empty lines
            
            # Add category and associated words to the categories dictionary
            categories[category] = words
    
    # Compile regular expression patterns for all categories
    patterns = {category: re.compile(r'\b(?:' + '|'.join(map(re.escape, words)) + r')\b', re.IGNORECASE)
                for category, words in categories.items()}
    
    # Combine patterns into a single regular expression
    combined_pattern = re.compile('|'.join(pattern.pattern for pattern in patterns.values()))
    
    # Initialize a set to store already tagged words
    tagged_words = set()

    # Tag words based on the category of the input text
    tagged_text = input_text
    for match in combined_pattern.finditer(tagged_text):
        matched_word = match.group()
        if matched_word not in tagged_words:
            for category in priority_order:
                if matched_word in patterns[category].pattern:
                    tagged_text = tagged_text.replace(matched_word, f'<{category}>{matched_word}</{category}>')
                    tagged_words.add(matched_word)
                    break  # Stop searching for categories once a match is found
    
    # Print the tagged text
    print(tagged_text)
    return tagged_text


import json
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# Input and output file paths
input_file_path = 'Data/test_150_tagged_en_ner_bc5cdr_md.jsonl'
output_file_path = 'Data/test_150_tagged_en_ner_bc5cdr_md_hard_coded.jsonl'
categories_folder = 'ChemFont_Tagger_Files'

# Priority order of categories
priority_order = ['source', 
                  'process', 
                  'disposition',
                  'exposure_root',
                  'health_effect',
                  'organoleptic_effect',
                  'role',
                  'food']

# Process each line in the input JSONL file
with open(input_file_path, 'r', encoding='utf-8') as input_file, \
     open(output_file_path, 'w', encoding='utf-8') as output_file:
    
    # Read lines from input file and create a list
    lines = list(input_file)

    # Function to process a single line
    def process_line(line):
        data = json.loads(line)
        input_text = data['input']
        tagged_text = tag_words_with_category(categories_folder, input_text, priority_order)
        data['input'] = tagged_text
        return json.dumps(data)

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor() as executor:
        # Process lines in parallel and track progress with tqdm
        for result in tqdm(executor.map(process_line, lines), total=len(lines)):
            output_file.write(result + '\n')