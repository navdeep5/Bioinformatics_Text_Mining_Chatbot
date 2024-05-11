import os
import json
from openai import OpenAI
from tqdm import tqdm

# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=INSERT_API_KEY,
)

# Function to generate abstracts
def generate_abstract(example_abstract, triples):
    # Prompt with example abstract and triples
    # prompt = f"""
    # You have been provided with the following information:

    # {triples}

    # You also have a sample abstract:

    # {example_abstract}

    # Write a new abstract, following the structure of the provided sample abstract, using the given information and incorporating the words: 'biolocation', 'role', 'sourced', 'involved', 'exposed', 'causes'.
    # """

    prompt = f"""
    You have been provided with the following information:

    {triples}

    Please generate a PubMed-like abstract based on the provided information. Your abstract should be between 250 and 750 words in length and should follow the structure commonly found in PubMed abstracts. However, make sure not to include the following words: 'biolocation', 'role', 'sourced', 'involved', 'exposed', 'causes'. Incorporate the information provided to create a coherent and informative abstract.
    """

    completion = client.chat.completions.create(
    model="openai/gpt-3.5-turbo",
    messages=[
        {
        "role": "user",
        "content": prompt,
        },
    ],
    )
    generated_abstract = completion.choices[0].message.content

    return generated_abstract

# # Function to process text files and generate abstracts
# def process_files(input_folder, triples_file, output_file):
#     with open(triples_file, 'r', encoding='utf-8') as triple_file, \
#          open(output_file, 'w', encoding='utf-8') as outfile:
        
#         # Iterate through text files and JSONL file simultaneously
#         for filename, line in zip(os.listdir(input_folder), triple_file):
#             if filename.endswith('.txt'):
#                 # Read example abstract from text file
#                 with open(os.path.join(input_folder, filename), 'r', encoding='utf-8') as f:
#                     example_abstract = f.read()

#                 # Read triples from JSONL file
#                 triples = json.loads(line.strip())

#                 triplet_str = ""
#                 for i in triples:
#                     triplet_str += ' '.join(i)
#                     if i != len(triples) - 2:
#                         triplet_str += " and "

#                 # Generate new abstract based on example abstract and triples
#                 generated_abstract = generate_abstract(example_abstract, triplet_str)

#                 # Write input-output pair to JSONL file
#                 json.dump({"input": generated_abstract, "output": triples}, outfile)
#                 outfile.write('\n')

# # Folder containing example abstracts
# input_folder = 'example_abstracts_folder'

# # JSONL file containing triples
# triples_file = 'triples.jsonl'

# # Output JSONL file
# output_file = 'generated_abstracts.jsonl'

# # Process text files and generate abstracts
# process_files(input_folder, triples_file, output_file)


# Function to process text files and generate abstracts
def process_files(input_folder, triples_file, output_file):
    with open(triples_file, 'r', encoding='utf-8') as triple_file, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        
        # Count the total number of lines in the triples file
        total_lines = sum(1 for _ in triple_file)
        # Reset the file pointer to the beginning of the file
        triple_file.seek(0)

        # Create a tqdm progress bar
        progress_bar = tqdm(total=total_lines, desc="Processing", unit="line")

        # Iterate through text files and JSONL file simultaneously
        for line in triple_file:
            # Update the tqdm progress bar
            progress_bar.update(1)

            # Read triples from JSONL file
            triples = json.loads(line.strip())

            triplet_str = ""
            for i in range(len(triples)):
                triplet_str += ' '.join(triples[i])
                if i < (len(triples) - 1):
                    triplet_str += " and "

            # Generate new abstract based on example abstract and triples
            generated_abstract = generate_abstract('example_abstract', triplet_str)

            # Write input-output pair to JSONL file
            json.dump({"input": generated_abstract, "output": triples}, outfile)
            outfile.write('\n')

# Folder containing example abstracts
input_folder = 'example_abstracts_folder'

# JSONL file containing triples
triples_file = 'Clusters/strict_correlated_clusters.jsonl'

# Output JSONL file
output_file = 'Abstract_Generation/gpt_abstract.jsonl'

# Process text files and generate abstracts
process_files(input_folder, triples_file, output_file)
