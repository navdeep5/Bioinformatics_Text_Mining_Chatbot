import pandas as pd
import json

def convert_to_jsonl(input_excel, output_jsonl):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(input_excel)

    # Open the output JSONL file for writing
    with open(output_jsonl, 'w') as f:
        # Iterate over each row in the DataFrame
        for index, row in df.iterrows():
            # Extract the title and text from the row
            title = row['Title']
            text = row['Text']

            # Combine the title and text into a single input string
            input_text = f"{title} {text}"

            # Extract the triplets from the row
            print(title)
            triplets = eval(str(row['Triplets']))

            # Create a dictionary containing the input and output
            data = {"input": input_text, "output": triplets}

            # Write the data dictionary as a JSON string to the output file
            f.write(json.dumps(data) + '\n')

# Example usage
input_excel = "Data/Real_Abstracts/_REAL_-Triplet extraction.xlsx"
output_jsonl = "Data/Real_Abstracts/real_abstracts_30.jsonl"
convert_to_jsonl(input_excel, output_jsonl)
