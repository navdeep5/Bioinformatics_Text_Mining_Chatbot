import os
import re

def tag_words_with_category(categories_folder, input_text, priority_order):
    # Initialize an empty dictionary to store categories and their associated words
    categories = {}

    # Process each file in the categories folder
    for filename in os.scandir(categories_folder):
        if filename.name.endswith('.txt') and filename.is_file():
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

# Example usage
categories_folder = 'ChemFont_tagger_Files'
input_text = """
    Bioconversion of Chitin into chitin oligosaccharides using a novel chitinase with high Chitin-binding capacity. Chitin is the second largest renewable biomass resource in nature, it can be enzymatically degraded into high-value chitin oligosaccharides (CHOSs) by chitinases. In this study, a chitinase (ChiC8-1) was purified and biochemically characterized, its structure was analyzed by molecular modeling. ChiC8-1 had a molecular mass of approximately 96 kDa, exhibited its optimal activity at pH 6.0 and 50  C. The Km and Vmax values of ChiC8-1 towards colloidal Chitin were 10.17 mgmL-1 and 13.32 U/mg, respectively. Notably, ChiC8-1 showed high Chitin-binding capacity, which may be related to the two Chitin binding domains in the N-terminal. Based on the unique properties of ChiC8-1, a modified affinity chromatography method, which combines protein purification with Chitin hydrolysis process, was developed to purify ChiC8-1 while hydrolyzing Chitin. In this way, 9.36 +- 0.18 g CHOSs powder was directly obtained by hydrolyzing 10 g colloidal Chitin with crude enzyme solution. The CHOSs were composed of 14.77-2.83 % Acetylglucosamine and 85.23-97.17 % N N-diacetylchitobiose at different enzyme-substrate ratio. This process simplifies the tedious purification and separation steps, and may enable its potential application in the field of green production of chitin oligosaccharides.
"""

priority_order = ['source', 
                  'chemical',
                  'process', 
                  'disposition',
                  'exposure_root',
                  'health_effect',
                  'organoleptic_effect',
                  'role',
                  'food']  # Specify the priority order of categories

tag_words_with_category(categories_folder, input_text, priority_order)



'''
import os
import re

def tag_words_with_category(categories_folder, input_text, priority_order):
    # Initialize an empty dictionary to store categories and their associated words
    categories = {}

    # Process each file in the categories folder
    for filename in os.scandir(categories_folder):
        if filename.name.endswith('.txt') and filename.is_file():
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
        for category, pattern in patterns.items():
            if match.group() in pattern.pattern and category in priority_order:
                tagged_text = tagged_text.replace(match.group(), f'<{category}>{match.group()}</{category}>')
                tagged_words.add(match.group())
    
    # Print the tagged text
    print(tagged_text)

# Example usage
categories_folder = 'ChemFont_tagger_Files'
# input_text = """
#     The apple is a fruit. Sodium chloride is a chemical compound used in cooking. Water is essential for life.
# """

input_text = """
    Bioconversion of Chitin into chitin oligosaccharides using a novel chitinase with high Chitin-binding capacity. Chitin is the second largest renewable biomass resource in nature, it can be enzymatically degraded into high-value chitin oligosaccharides (CHOSs) by chitinases. In this study, a chitinase (ChiC8-1) was purified and biochemically characterized, its structure was analyzed by molecular modeling. ChiC8-1 had a molecular mass of approximately 96 kDa, exhibited its optimal activity at pH 6.0 and 50  C. The Km and Vmax values of ChiC8-1 towards colloidal Chitin were 10.17 mgmL-1 and 13.32 U/mg, respectively. Notably, ChiC8-1 showed high Chitin-binding capacity, which may be related to the two Chitin binding domains in the N-terminal. Based on the unique properties of ChiC8-1, a modified affinity chromatography method, which combines protein purification with Chitin hydrolysis process, was developed to purify ChiC8-1 while hydrolyzing Chitin. In this way, 9.36 +- 0.18 g CHOSs powder was directly obtained by hydrolyzing 10 g colloidal Chitin with crude enzyme solution. The CHOSs were composed of 14.77-2.83 % Acetylglucosamine and 85.23-97.17 % N N-diacetylchitobiose at different enzyme-substrate ratio. This process simplifies the tedious purification and separation steps, and may enable its potential application in the field of green production of chitin oligosaccharides.
"""

priority_order = ['source', 
                  'chemical',
                  'process', 
                  'disposition',
                  'exposure_root',
                  'health_effect',
                  'organoleptic_effect',
                  'role',
                  'food']  # Specify the priority order of categories

tag_words_with_category(categories_folder, input_text, priority_order)
'''