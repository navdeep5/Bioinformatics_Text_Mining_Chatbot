import json

# Define the instruction template
instruction_template = """
    The task is to extract chemical-related triples from scientific research papers.
    The rules are:
    1. Only use the following predicates in the triple: “causes”, ”biolocation is”, “exposed through”, “sourced through”, “has role of”, “involved in”.
    2. If there is more than one noun in the object, separate it into multiple triples.
    3. If you don't find relevant chemical-related triples in the paper or you are not sure, return: null.
    4. The response is an array of the relevant triples in the form: [subject, predicate, object].
    Q: Interaction of TMPC with ANXA2 mediated attachment and colonization of S. anginosus and induced mitogen-activated protein kinase (MAPK) activation.
    A: ["TMPC", "involved in", "MAPK activation"],
    ["ANXA2", "involved in", "MAPK activation"]
    Q: α-Lipoic acid plays an essential role in mitochondrial dehydrogenase reactions.
    A: ["alpha-Lipoic acid", "involved in", "mitochondrial dehydrogenase reactions"]
    Q: Ferroptosis, a form of regulated cell death that is driven by iron-dependent phospholipid peroxidation, has been implicated in multiple diseases, including cancer
    A: ["Ferroptosis", "causes", "cancer"]
    Q: These transporters and other biotin-binding proteins partition biotin to the cytoplasm and mitochondria cell compartments.
    A: ["Biotin", "biolocation is", "cytoplasm"],
    ["Biotin", "biolocation is", "mitochondria"]
"""

bio_prompt = '''Context: I want you to extract semantic triples from the following paragraph.
Rules: The subject of each triple is a chemical. Only use information explicitly present in the paragraph, do not hallucinate. Do not create any fictional or incorrect outputs. Strictly follow all rules and guidelines given. If the object of the triple has more than one noun, split it into separate triples with only one noun each. Do not repeat any triples. The output must be a list of the triples you are most confident in, with each triple in the format [“subject”, “predicate”, “object”].
Q: Extract triples on the part of the human body the chemical subjects can be found in. Use the predicate "biolocation is" for these triples. The object of each triple must be a human body part. If you cannot find any information on this, do not output any triples.'''
exp_prompt = 'Q: Extract triples on the human exposure route of the chemical subjects. Use the predicate "exposed through" for these triples. If you cannot find any information on this, do not output any triples.'
source_prompt = 'Q: Extract triples on what food or organism the chemical subject is sourced from. Use the predicate "sourced through" for these triples. If you cannot find any information on this, do not output any triples.'
dis_prompt = 'Q: Extract triples on what disease the chemical subject causes. Use the predicate "causes" for these triples. The object of each triple must be a disease. If you cannot find any information on this, do not output any triples.'
inv_prompt = 'Q: Extract triples on the biological mechanism the chemical subject is a part of. Use the predicate "involved in" for these triples. If you cannot find any information on this, do not output any triples.'
role_prompt = 'Q: Extract triples on the biological role the chemical subject has. Use the predicate "has role of" for these triples. If you cannot find any information on this, do not output any triples. Paragraph: '

combined_prompt = bio_prompt + exp_prompt + source_prompt + dis_prompt + inv_prompt + role_prompt
instruction_template = combined_prompt


# Path to the input JSONL file
input_file_path = "Data/gpt_mixtral_instructions_train_tagged_NoOE_karan.jsonl"

# Path to the output JSONL file
output_file_path = "Data/gpt_mixtral_instructions_train_tagged_NoOE_karan_2.jsonl"

# Open input and output files with utf-8 encoding
with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', encoding='utf-8') as output_file:
    # Loop through each line in the input file
    for line in input_file:
        # Parse the JSON from the line
        data = json.loads(line)
        
        # Add the "instruction" key with its value
        data['instruction'] = instruction_template.strip()
        # data['output'] = str(data['output'])
        
        # Write the modified JSON back to the output file
        output_file.write(json.dumps(data) + '\n')
