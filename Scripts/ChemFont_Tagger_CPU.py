import os
import re
import json
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import time

def load_categories(categories_folder):
    categories = {}
    for filename in os.scandir(categories_folder):
        if filename.name.endswith('.txt') and filename.is_file():
            category = os.path.splitext(filename.name)[0]
            with open(filename.path, 'r', encoding='utf-8') as file:
                words = {line.strip() for line in file if line.strip()}
            categories[category] = words
    return categories

def compile_patterns(categories):
    patterns = {}
    for category, words in categories.items():
        pattern = re.compile(r'\b(' + '|'.join(map(re.escape, words)) + r')\b', re.IGNORECASE)
        patterns[category] = pattern
    return patterns

def tag_text(input_text, categories, patterns):
    tagged_text = input_text
    for category, pattern in patterns.items():
        tagged_text = pattern.sub(lambda match: f'<{category}>{match.group()}</{category}>', tagged_text)
    return tagged_text

def process_line(line, categories, patterns):
    data = json.loads(line)
    input_text = data['input']
    tagged_text = tag_text(input_text, categories, patterns)
    data['input'] = tagged_text
    return json.dumps(data)


def main():
    input_file_path = 'C:/Users/navde/Desktop/Bioinformatics_401_Project/Data/test_150.jsonl'
    output_file_path = 'C:/Users/navde/Desktop/Bioinformatics_401_Project/Data/a.jsonl'
    categories_folder = 'C:/Users/navde/Desktop/Bioinformatics_401_Project/ChemFont_Tagger_Files'
    priority_order = ['source', 'process', 'disposition', 'exposure_root', 'health_effect', 'organoleptic_effect', 'role', 'food']

    print("Compile categories...")
    categories = load_categories(categories_folder)
    patterns = compile_patterns(categories)

    tic = time.time()

    print("Start reading and writing file...")
    with open(input_file_path, 'r', encoding='utf-8') as input_file, \
         open(output_file_path, 'w', encoding='utf-8') as output_file:
        
        lines = list(input_file)

        with ThreadPoolExecutor() as executor:
            results = list(tqdm(executor.map(lambda line: process_line(line, categories, patterns), lines), total=len(lines)))

        for result in results:
            output_file.write(result + '\n')

    tac = time.time()
    print("Elapsed time:", tac - tic, "seconds")




if __name__ == "__main__":
    main()
    # Provided string
    # input_text = """
    # Title: Green Tea Components and Their Potential Role in Human Health

    # Abstract: Green tea has been widely recognized for its numerous health benefits and potential therapeutic effects. This review focuses on six key components sourced through green tea, including (5Z)-(15S)-11-α-hydroxy-9,15-dioxoprosta-13-enoate, Cannogenol 3-[glucosyl-(1->4)-2,6-dideoxy-xylohexoside], cis-Zeatin-7-N-glucoside, Vinaginsenoside R7, (R)-lipoate, and Testosterone. These compounds have been shown to exhibit various biological activities, such as antioxidant, anti-inflammatory, and anticancer properties.

    # The first compound, (5Z)-(15S)-11-α-hydroxy-9,15-dioxoprosta-13-enoate, has been found to possess antioxidant and anti-inflammatory effects. It has been suggested that this compound may play a role in protecting cells from oxidative stress and inflammation. Cannogenol 3-[glucosyl-(1->4)-2,6-dideoxy-xylohexoside], another green tea component, has been shown to exhibit antioxidant and anti-inflammatory activities as well. It may also have potential in the treatment of neurodegenerative diseases.

    # Cis-Zeatin-7-N-glucoside is another green tea component with potential health benefits. This compound has been found to have anticancer properties and may be useful in the treatment of various cancers. Vinaginsenoside R7 is another antioxidant compound found in green tea. It has been shown to have potential in the treatment of diabetes and cardiovascular diseases.

    # (R)-lipoate is another green tea component with antioxidant properties. It has been found to protect cells from oxidative stress and may have potential in the treatment of neurodegenerative diseases. Lastly, Testosterone is a hormone found in green tea and has been shown to have potential in the treatment of male reproductive disorders.

    # In conclusion, green tea components such as (5Z)-(15S)-11-α-hydroxy-9,15-dioxoprosta-13-enoate, Cannogenol 3-[glucosyl-(1->4)-2,6-dideoxy-xylohexoside], cis-Zeatin-7-N-glucoside, Vinaginsenoside R7, (R)-lipoate, and Testosterone have been shown to exhibit various biological activities and may have potential in the treatment of various diseases. Further research is needed to fully understand their mechanisms of action and potential therapeutic applications.
    # """

    # # Categories folder
    # categories_folder = 'C:/Users/navde/Desktop/Bioinformatics_401_Project/ChemFont_Tagger_Files'

    # # Priority order of categories
    # priority_order = ['source', 'process', 'disposition', 'exposure_root', 'health_effect', 'organoleptic_effect', 'role', 'food']

    # # Load categories
    # print("Loading categories...")
    # categories = load_categories(categories_folder)
    # patterns = compile_patterns(categories)

    # # Tag the provided text
    # print("Getting result...")
    # tagged_text = tag_text(input_text, categories, patterns)
    # print(tagged_text)
