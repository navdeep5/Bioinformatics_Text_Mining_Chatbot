import json
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def replace_tags_in_string(input_string):
    replacements = {
        '<CHEMICAL>': 'the chemical known as ',
        '<disposition>': 'the disposition known as ',
        '<exposure_root>': 'the exposure route known as ',
        '<food>': 'the food known as ',
        '<health_effect>': 'the health effect known as ',
        '<organoleptic_effect>': 'the organoleptic effect known as ',
        '<process>': 'the process known as ',
        '<role>': 'the role known as ',
        '<source>': 'the source known as ',
        '<DISEASE>': 'the disease known as',
    }

    # Replace each tag with its corresponding phrase
    for tag, replacement in replacements.items():
        input_string = input_string.replace(tag, replacement)
        # Remove the closing tags as well
        input_string = input_string.replace('</' + tag[1:], '')

    # Capitalize the first letter of each sentence
    sentences = input_string.split('. ')
    sentences = [sentence.capitalize() for sentence in sentences]

    # Join the sentences back together
    output_string = '. '.join(sentences)

    return output_string

def process_abstracts(abstracts):
    results = []
    for abstract in tqdm(abstracts, desc="Processing Abstracts"):
        result = replace_tags_in_string(abstract)
        results.append(result)
    return results

def process_jsonl(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = [json.loads(line) for line in f.readlines()]

    for item in tqdm(data, desc="Processing JSONL File"):
        item['input'] = replace_tags_in_string(item['input'])

    with open(output_file, 'w', encoding='utf-8') as f:
        for item in tqdm(data, desc="Writing Output JSONL"):
            f.write(json.dumps(item) + '\n')

# Test the functions
# input_string = "\n\nTitle: Diverse Bioactive Compounds Sourced from <source>Devilfish</source>: A Comprehensive Review\n\nBackground: The diverse bioactive compounds found in <source>Devilfish</source> have been attracting significant attention in recent years due to their potential applications in various fields such as <organoleptic_effect>medicine</organoleptic_effect>, cosmetics, and <role>agriculture</role>. This review aims to provide an overview of the various bioactive compounds sourced from <source>Devilfish</source> and their potential uses.\n\nMethods: A comprehensive literature search was conducted to identify and compile information on bioactive compounds found in <source>Devilfish</source>. The search included databases such as PubMed, Web of Science, and Google Scholar. The identified sources were then analyzed to extract relevant information on the compounds and their potential applications.\n\nResults: Several bioactive compounds have been identified in <source>Devilfish</source>, including GDP-\u03b1-D-mannose, <organoleptic_effect>Eugenol</organoleptic_effect>, Spermidine, 2-18:2(9Z,12Z)-lysophosphatidylcholine, (+)-pulegone, and 3-Indoleacetonitrile. These compounds have been found to exhibit various <source>biological</source> activities such as <role>antioxidant</role>, <role>anti-inflammatory</role>, anticancer, and antimicrobial properties.\n\nConclusion: The diverse bioactive compounds found in <source>Devilfish</source> have significant potential in various industries and applications. Further research is needed to fully understand their mechanisms of action and optimize their extraction and utilization. This review provides an overview of the current knowledge on bioactive compounds sourced from <source>Devilfish</source> and their potential applications, which can serve as a foundation for future research and development efforts."

# output_string = replace_tags_in_string(input_string)
# print(output_string)

input_file = 'Data/Tagging_Data/Tagging_50_Test.jsonl'
output_file = 'Data/Tagging_Data/Sentence_Tagging_50_Test.jsonl'
process_jsonl(input_file, output_file)
