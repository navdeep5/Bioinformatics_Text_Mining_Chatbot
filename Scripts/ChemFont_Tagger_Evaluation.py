import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score
from tqdm import tqdm
import json
import re

def extract_tags(text):
    # Regular expression to match substrings enclosed within <>
    pattern = r'<([^<]*?)>(.*?)<\/\1>'

    # Find all tagged substrings
    tagged_substrings = re.findall(pattern, text)

    # Return each tag and content separately
    tagged_lists = [[tag, content] for tag, content in tagged_substrings]

    return tagged_lists

def calculate_scores(outputs, ground_truths):
    f1_scores = []
    precision_scores = []
    recall_scores = []
    for output, ground_truth in tqdm(zip(outputs, ground_truths), total=len(outputs)):
        # Convert lists of tuples to lists of strings
        output_strings = [' '.join(map(str, item)).lower() for item in output]
        ground_truth_strings = [' '.join(map(str, item)).lower() for item in ground_truth]
        
        # Calculate scores
        f1 = f1_score(output_strings, ground_truth_strings, average='micro')
        precision = precision_score(output_strings, ground_truth_strings, average='micro')
        recall = recall_score(output_strings, ground_truth_strings, average='micro')
        
        # # Append scores to lists
        # f1_scores.append(f1)
        # precision_scores.append(precision)
        # recall_scores.append(recall)
    
    # return f1_scores, precision_scores, recall_scores
    return f1, precision, recall

def print_statistics(scores):
    print("Minimum:", np.min(scores))
    print("Maximum:", np.max(scores))
    print("Average:", np.mean(scores))
    print("Standard Deviation:", np.std(scores))


# Run script
f1_score_list = []
precision_list = []
recall_list = []
jw_score_list = []

test_set_path = 'Data/Tagging_50_Test.jsonl'
truth_file_path = 'Data/Tagging_Ground_Truth_Bias.jsonl'

with open(test_set_path, 'r',encoding="utf-8") as infile, open(truth_file_path, "r",encoding="utf-8") as outfile:
    for line, gt_line in tqdm(zip(infile, outfile)):
        data = json.loads(line)
        datagt = json.loads(gt_line)
        abstract = data['input']
        ground_truth = datagt['input']

        # print(extract_tags(abstract))
        # print(extract_tags(ground_truth))

        # Get scores
        f1_value, precision, recall = calculate_scores(extract_tags(abstract), extract_tags(ground_truth))

        #Increment variables
        f1_score_list.append(f1_value)
        precision_list.append(precision)
        recall_list.append(recall)

print("F1 Score:")
print_statistics(f1_score_list)
print("\nPrecision:")
print_statistics(precision_list)
print("\nRecall:")
print_statistics(recall_list)
