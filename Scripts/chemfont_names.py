# import json
# from tqdm import tqdm

# name_set = set()

# # Function to read JSONL file and process each JSON object
# def read_jsonl(filename):
#     with open(filename, 'r', encoding='utf-8') as file:
#         # Count the total number of lines in the file for tqdm
#         total_lines = sum(1 for line in file)
#         # Reset the file pointer to the beginning of the file
#         file.seek(0)
#         # Use tqdm to track progress
#         for line in tqdm(file, total=total_lines, desc='Processing JSONL'):
#             # Load JSON object from each line
#             data = json.loads(line)
#             # Extract 'output' key from JSON object
#             output_list = data.get('output', [])
#             # Iterate through output list
#             for item in output_list:
#                 # name_set.add(item[0])
#                 # name_set.add(item[2])
#                 name_set.add((item[0], item[2]))

# # Provide the filename of the JSONL file
# filename = 'Data/test_data.jsonl'
# # Call the function to read and process the JSONL file
# read_jsonl(filename)

# # Write to a text file
# fails = 0
# with open("chemfont_names_abstracts.txt", "w") as file:
#     for name in name_set:
#         try:
#             file.write(str(name) + "\n")
#         except:
#             fails += 1
# print(f"Total fails: {fails}")



import json
from tqdm import tqdm

name_set = set()

# Function to read JSONL file and process each JSON object
def read_jsonl(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        # Count the total number of lines in the file for tqdm
        total_lines = sum(1 for line in file)
        # Reset the file pointer to the beginning of the file
        file.seek(0)
        # Use tqdm to track progress
        for line in tqdm(file, total=total_lines, desc='Processing JSONL'):
            # Iterate through  list
            triplet = json.loads(line)

            # Iterate through triplet 
            name_set.add((triplet[0], triplet[2]))

# Provide the filename of the JSONL file
filename = 'Triplets_replacement_unique/merged_triplets.jsonl'
# Call the function to read and process the JSONL file
read_jsonl(filename)

# Write to a text file
fails = 0
with open("chemfont_names_all.txt", "w") as file:
    for name in name_set:
        try:
            file.write(str(name) + "\n")
        except:
            fails += 1
print(f"Total fails: {fails}")
