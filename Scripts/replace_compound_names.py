import json
import argparse
import re
from tqdm import tqdm

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
    "LysoPA": "lysophosphatidic acid",
    "LPA": "lysophosphatidic acid"
}

    # Function to replace the first string in each line
    def replace_first_string(input_list):
        code = input_list[0]
        code_end = input_list[2]
        result = ["nan", input_list[1], "nan"]
        for key in mapping.keys():
            if key == code[:len(key)]:
                result[0] = mapping[key]
                # return [mapping[key]] + input_list[1:]

            if key == code_end[:len(key)]:
                result[2] = (mapping[key])
                # return [mapping[key]] + input_list[1:]

        if "nan" in result:
            for i in range(3):
                if result[i] == "nan":
                    result[i] = input_list[i]
        return result 


    # Read the JSONL file, replace the first string, and write to a new file
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        lines = infile.readlines()
        for line in tqdm(lines, desc="Processing", unit=" lines"):
            data = json.loads(line)
            modified_data = replace_first_string(data)
            outfile.write(json.dumps(modified_data) + '\n')

    print(f"Replacement completed. Check {output_file} for the result.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Required parameters
    parser.add_argument(
        "--input_file", default=None, type=str, required=True, help="Input JsonL."
    )

    parser.add_argument(
        "--output_file", default=None, type=str, required=True, help="Output JsonL."
    )

    args = parser.parse_args()
    do_replacement(args.input_file, args.output_file)