import json
import argparse
import re
from tqdm import tqdm
import ast

def do_replacement(input_file, output_file):
    # Define the mapping
    mapping = {
    "De Novo Triac": "triacylglycerol biosynthesis",
    "Cardiolipin Biosynthesis CL": "cardiolipin biosynthesis",
    "Triacylglycerol M": "triacylglycerol metabolism ",
    "Phosphatidylethanolamine Bio": "phophatidylethanolamine biosynthesis",
    "Phosphatidylcholine/Ph": "phosphatidylcholine and phophatidylethanolamine biosynthesis",
    "Phospholipid Bio": "phospholipid biosynthesis",
    "Phosphatidylcholine Bio": "phosphatidylcholine biosynthesis",
    "Triacylglycerol Deg": "triacylglycerol degradation",
    "TG": "triacylglycerol",
    "LysoPC": "lysophospholipid",
    "PS": "phosphatidylserine",
    "PG": "phosphatidylglycerol",
    "PI": "phosphatidylinositol",
    "DG": "diglyceride",
    "Cer": "ceramide",
    "CL": "cardiolipin",
    "PE": "phophatidylethanolamine",
    "PIP": "phosphatidylinositol phosphate",
    "SM": "sphingomyelin",
    "PC": "phosphatidylcholine",
    "PA": "phosphatidic acid",
    "LysoPA": "lysophosphatidic acid"
}

    # Function to replace the first string in each line
    def replace_first_string(input_list):
        code = input_list
        print(code)
        for key in mapping.keys():
            if key == code[:len(key)]:
                # return [mapping[key]] + input_list[1:]
                return (mapping[key] + '\n')
        return input_list 


    # Read the JSONL file, replace the first string, and write to a new file
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        lines = infile.readlines()
        for line in tqdm(lines, desc="Processing", unit=" lines"):
            modified_data = replace_first_string(line)
            outfile.write(str(modified_data))

    print(f"Replacement completed. Check {output_file} for the result.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Required parameters
    parser.add_argument(
        "--input_file", default=None, type=str, required=True, help="Input test."
    )

    parser.add_argument(
        "--output_file", default=None, type=str, required=True, help="Output test."
    )

    args = parser.parse_args()
    do_replacement(args.input_file, args.output_file)