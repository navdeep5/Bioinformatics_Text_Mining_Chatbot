import json
from tqdm import tqdm
import pandas as pd
import numpy as np

SENTENCE_PHRASES = ["the chemical known as", "the source known as", "the role known as", 
                   "the disposition known as", "the diseaese known as", "the health effect known as", 
                   "the process known as", "the exposure route known as", "the food known as",
                   "the organoleptic effect known as"]

HTML_PHRASES = ["<CHEMICAL>", "<source>", "<role>",
                "<disposition>", "<DISEASE>", "<health_effect>",
                "<process>", "<exposure_root>", "<food>",
                "<organoleptic_effect>"]

def load_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = [json.loads(line) for line in file]
    return data

def compute_metrics(true_positives, false_positives, false_negatives):
    # Initialize lists to store scores
    precision_scores = []
    recall_scores = []
    f1_scores = []

    # Iterate through each row
    for index in tqdm(range(len(true_positives)), desc="Processing rows"):
        # Skip rows if within skip_ranges

        true_positives_flat = true_positives[index]
        false_positives_flat = false_positives[index]
        false_negatives_flat = false_negatives[index]
            
        # Compute Original Scores
        # Compute precision
        precision = len(true_positives_flat) / (len(true_positives_flat) + len(false_positives_flat)) if (len(true_positives_flat) + len(false_positives_flat)) > 0 else 0
        precision_scores.append(precision)

        # Compute recall
        recall = len(true_positives_flat) / (len(true_positives_flat) + len(false_negatives_flat)) if (len(true_positives_flat) + len(false_negatives_flat)) > 0 else 0
        recall_scores.append(recall)

        # Compute F1-score
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        f1_scores.append(f1)


    # Compute statistics
    metrics = {
        "Precision": precision_scores,
        "Recall": recall_scores,
        "F1-score": f1_scores
    }

    for metric, scores in metrics.items():
        avg = np.mean(scores)
        minimum = np.min(scores)
        maximum = np.max(scores)
        std = np.std(scores)
        
        # Print statistics
        print(metric + ":")
        print("  Average:", avg)
        print("  Minimum:", minimum)
        print("  Maximum:", maximum)
        print("  Standard Deviation:", std)
        print()   
    
    print(f"Total Length: {len(f1_scores)}")

def extract_phrases(data):
    phrases = []
    text = data.lower()
    
    for phrase in HTML_PHRASES:
        index = 0
        while index < len(text):
            if phrase in text[index:]:
            # Find the index of the phrase
                index = text[index:].find(phrase) + index
                # Extract the phrase and the next two words
                remaining_chars = len(text) - index - len(phrase)
                phrase_context = text[index:index + len(phrase) + min(50, remaining_chars)]
                phrases.append(phrase_context.lower())
                index += len(phrase)
            else:
                break
    return phrases


def calculate_confusion_lists(output_phrases, ground_truth_phrases):
    # Initate lists
    true_positives = []
    false_positives = []
    false_negatives = []
    
    # Classify each item
    for phrase_out in output_phrases:
        # Check if any part of the output triplet partially matches any part of the ground truth triplet
        if (phrase_out in ground_truth_phrases):
            index = ground_truth_phrases.index(phrase_out)
            true_positives.append(ground_truth_phrases[index])
        else:
            false_positives.append(phrase_out)

    for phrase_gt in ground_truth_phrases:
        # Check if any part of the ground truth triplet partially matches any part of the output triplet
        if (phrase_gt not in output_phrases):
            false_negatives.append(phrase_gt)
    


    return true_positives, false_positives, false_negatives

# Load the ground truth and output data from JSONL files
ground_truth = load_jsonl("Data/Tagging_Data/Tagging_Ground_Truth_Bias.jsonl")
output = load_jsonl("Data/Tagging_Data/Tagging_50_Test.jsonl")

count = 0
true_positives_list = []
false_positives_list = []
false_negatives_list = []

# Iterate through jsonl files
for item_gt, item_out in zip(ground_truth, output):
    # Extract phrases from the ground truth and output data
    ground_truth_phrases = extract_phrases(item_gt['input'])
    output_phrases = extract_phrases(item_out['input'])

    # Calculate confusion lists
    true_positives, false_positives, false_negatives = calculate_confusion_lists(output_phrases, ground_truth_phrases)
    true_positives_list.append(true_positives)
    false_positives_list.append(false_positives)
    false_negatives_list.append(false_negatives)

    if len(false_negatives) >= 1:
    #     print("True Positives:" + str((true_positives)))
    #     print("False Positives:" + str((false_positives)))
    #     print("False Negatives:" + str((false_negatives)))
    #     print()
    #     print()
        count += 1
print(count)

# Compute metrics
compute_metrics(true_positives_list, false_positives_list, false_negatives_list)

   


# # Output the results
# print("True Positives:")
# for tp in true_positives:
#     print(tp)
# print("\nFalse Positives:")
# for fp in false_positives:
#     print(fp)
# print("\nFalse Negatives:")
# for fn in false_negatives:
#     print(fn)
