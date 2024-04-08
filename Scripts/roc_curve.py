# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.metrics import roc_curve, auc

# # Example of binary information (0: negative, 1: positive)
# # Replace these with your actual binary predictions and ground truth
# # Assume each sublist represents a unique prediction
# # Here, 'output' represents the model's predictions and 'ground_truth' represents the true labels
# output = [0, 1, 0, 1, 1, 0, 0, 1, 0, 1]
# ground_truth = [0, 1, 0, 1, 1, 0, 1, 1, 0, 1]

# # Calculate ROC curve
# fpr, tpr, thresholds = roc_curve(ground_truth, output)

# # Compute AUROC (Area Under the ROC Curve)
# roc_auc = auc(fpr, tpr)

# # Plot ROC curve
# plt.figure()
# plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
# plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
# plt.xlim([0.0, 1.0])
# plt.ylim([0.0, 1.05])
# plt.xlabel('False Positive Rate')
# plt.ylabel('True Positive Rate')
# plt.title('Receiver Operating Characteristic (ROC) Curve')
# plt.legend(loc="lower right")
# plt.show()

# # Output AUROC
# print("AUROC:", roc_auc)



# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.metrics import roc_curve, auc

# # Output and Ground Truth lists
# output = [['LPA(0:0/18:2(9Z,12Z))', 'involved in', 'Cardiolipin Biosynthesis CL(16:0/16:0/20:3(5Z,8Z,11Z)/20:4(8Z,11Z,14Z,17Z))'],
#           ['LPA(0:0/18:2(9Z,12Z))', 'involved in', 'De Novo Triacylglycerol Biosynthesis TG(i-20:0/a-17:0/18:0)'],
#           ['LPA(0:0/18:2(9Z,12Z))', 'involved in', 'De Novo Triacylglycerol Biosynthesis TG(18:3(6Z,9Z,12Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:1(13Z))']]

# ground_truth = [["LPA(0:0/18:2(9Z,12Z))", "involved in", "Cardiolipin Biosynthesis CL(16:0/16:0/20:3(5Z,8Z,11Z)/20:4(8Z,11Z,14Z,17Z))"],
#                 ["LPA(0:0/18:2(9Z,12Z))", "involved in", "De Novo Triacylglycerol Biosynthesis TG(i-20:0/a-17:0/18:0)"],
#                 ["LPA(0:0/18:2(9Z,12Z))", "involved in", "De Novo Triacylglycerol Biosynthesis TG(18:3(6Z,9Z,12Z)/20:5(5Z,8Z,11Z,14Z,17Z)/22:1(13Z))"]]

# # Function to convert each list into a binary list
# def to_binary(output, ground_truth):
#     binary_output = []
#     binary_ground_truth = []
#     for item in output:
#         if item in ground_truth:
#             binary_output.append(1)
#         else:
#             binary_output.append(0)
#     for item in ground_truth:
#         if item in output:
#             binary_ground_truth.append(1)
#         else:
#             binary_ground_truth.append(0)
#     return binary_output, binary_ground_truth

# # Convert lists to binary
# binary_output, binary_ground_truth = to_binary(output, ground_truth)
# print(binary_output)
# print(binary_ground_truth)

# # Compute ROC curve and AUC
# fpr, tpr, thresholds = roc_curve(binary_ground_truth, binary_output)
# roc_auc = auc(fpr, tpr)

# # Plot ROC curve
# plt.figure()
# plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
# plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
# plt.xlim([0.0, 1.0])
# plt.ylim([0.0, 1.05])
# plt.xlabel('False Positive Rate')
# plt.ylabel('True Positive Rate')
# plt.title('Receiver Operating Characteristic')
# plt.legend(loc='lower right')
# plt.show()

# # Print AUC
# print("Area under ROC curve:", roc_auc)



# import json
# import numpy as np
# from sklearn.metrics import roc_curve, auc
# import matplotlib.pyplot as plt
# from tqdm import tqdm
# import ast

# def parse_jsonl(output_file_path, ground_truth_file_path):
#     outputs = []
#     ground_truths = []
#     with open(output_file_path, 'r',encoding="utf-8") as output_file, open(ground_truth_file_path, "r",encoding="utf-8") as gt_file:
#         for line, gt_line in tqdm(zip(output_file, gt_file), desc="Reading JSONL", unit=" lines"):
#             data = json.loads(line)
#             if data['valid'] == True:
#                 gt_data = json.loads(gt_line)
#                 outputs.extend(ast.literal_eval(data['output']))
#                 ground_truths.extend(gt_data['output'])
#     return outputs, ground_truths

# def calculate_scores(outputs, ground_truths):
#     binary_labels = []
#     scores = []
#     for output, ground_truth in tqdm(zip(outputs, ground_truths), total=len(outputs), desc="Calculating scores", unit=" instances"):
#         print(f"Output: {output}")
#         print(f"Ground Truth: {ground_truth}")
#         binary_labels.append(1 if output in ground_truth else 0)
#         scores.append(1)  # Assigning a score of 1 for simplicity, since all instances are positive
#     return binary_labels, scores

# def plot_roc_curve(binary_labels, scores):
#     fpr, tpr, _ = roc_curve(binary_labels, scores)
#     roc_auc = auc(fpr, tpr)
#     plt.figure()
#     plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
#     plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
#     plt.xlim([0.0, 1.0])
#     plt.ylim([0.0, 1.05])
#     plt.xlabel('False Positive Rate')
#     plt.ylabel('True Positive Rate')
#     plt.title('Receiver Operating Characteristic (ROC) Curve')
#     plt.legend(loc='lower right')
#     plt.show()

# if __name__ == "__main__":
#     output_file_path = "Evaluation/Vanilla_Untagged/output_vanilla_untagged.jsonl" 
#     ground_truth_file_path = "Data/test_150.jsonl"
#     outputs, ground_truths = parse_jsonl(output_file_path, ground_truth_file_path)
#     binary_labels, scores = calculate_scores(outputs, ground_truths)
#     plot_roc_curve(binary_labels, scores)


# import json
# import numpy as np
# from sklearn.metrics import roc_curve, auc
# import matplotlib.pyplot as plt
# from tqdm import tqdm
# import ast

# def parse_jsonl(output_file_path, ground_truth_file_path):
#     binary_labels = []
#     scores = []
#     with open(output_file_path, 'r', encoding="utf-8") as output_file, open(ground_truth_file_path, "r", encoding="utf-8") as gt_file:
#         for line, gt_line in tqdm(zip(output_file, gt_file), desc="Reading JSONL", unit=" lines"):
#             data = json.loads(line)
#             if data['valid'] == True:
#                 gt_data = json.loads(gt_line)
#                 output = ast.literal_eval(data['output'])
#                 ground_truth = gt_data['output']
#                 # print(f"Output: {output}")
#                 # print(f"Ground Truth: {ground_truth}")
#                 # for item in output:
#                 #     binary_labels.append(1 if item in ground_truth else 0)
#                 #     scores.append(1)  # Assigning a score of 1 for simplicity, since all instances are positive


#                 # for item_index, item in enumerate(output):
#                 #     # Check if the item is in the ground truth
#                 #     if item in ground_truth:
#                 #         binary_labels.append(1)  # Positive label
#                 #     else:
#                 #         binary_labels.append(0)  # Negative label
#                 #     # Assign score based on the rank of the prediction
#                 #     score = 1 - (item_index / len(output))  # Example: higher score for earlier predictions
#                 #     scores.append(score)

#                 for item_index, item in enumerate(output):
#                     # Check if the item is in the ground truth
#                     if item in ground_truth:
#                         binary_labels.append(1)  # Positive label
#                     else:
#                         binary_labels.append(0)  # Negative label
#                     # Assign score based on the rank of the prediction
#                     scores.append(1 - (item_index / len(output)))
#     return binary_labels, scores

# def plot_roc_curve(binary_labels, scores):
#     fpr, tpr, _ = roc_curve(binary_labels, scores)
#     roc_auc = auc(fpr, tpr)
#     plt.figure()
#     plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
#     plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
#     plt.xlim([0.0, 1.0])
#     plt.ylim([0.0, 1.05])
#     plt.xlabel('False Positive Rate')
#     plt.ylabel('True Positive Rate')
#     plt.title('Receiver Operating Characteristic (ROC) Curve')
#     plt.legend(loc='lower right')
#     plt.show()

# if __name__ == "__main__":
#     output_file_path = "Evaluation/Vanilla_Tagged/output_vanilla_tagged.jsonl" 
#     ground_truth_file_path = "Data/test_150.jsonl"
#     binary_labels, scores = parse_jsonl(output_file_path, ground_truth_file_path)
#     print(binary_labels)
#     plot_roc_curve(binary_labels, scores)



import json
import numpy as np
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
from tqdm import tqdm
import ast

def parse_jsonl(output_file_path, ground_truth_file_path):
    binary_labels = []
    scores = []
    with open(output_file_path, 'r', encoding="utf-8") as output_file, open(ground_truth_file_path, "r", encoding="utf-8") as gt_file:
        for line, gt_line in tqdm(zip(output_file, gt_file), desc="Reading JSONL", unit=" lines"):
            data = json.loads(line)
            if data['valid'] == True:
                gt_data = json.loads(gt_line)
                output = ast.literal_eval(data['output'])
                ground_truth = gt_data['output']
                # Call to_binary function to binarize predictions
                output_binary, target_binary = to_binary(output, ground_truth)
                binary_labels.extend(output_binary)
                scores.extend(target_binary)  # Assign a score of 1 for simplicity
    return binary_labels, scores

def to_binary(preds, gt):
    gt = [tuple(item.lower() for item in element) for element in gt]
    preds = [tuple(item.lower() for item in element) for element in preds]
    gt = set(gt)
    preds = set(preds)
    output = []
    target = []
    for pred in preds:
        # model is saying positive
        output.append(1)

        # is the model correct?
        if pred in gt:
            # real triplet (true positive)
            gt.remove(pred)
            target.append(1)
        else:
            # fake triplet (false positive)
            target.append(0)

    # if gt is not empty, model missed some!
    # unextracted triplets (false negatives)
    target.extend([1 for item in gt])
    output.extend([0 for item in gt])
    
    return output, target

def plot_roc_curve(binary_labels, scores):
    fpr, tpr, _ = roc_curve(binary_labels, scores)
    roc_auc = auc(fpr, tpr)
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc='lower right')
    plt.show()

if __name__ == "__main__":
    output_file_path = "Evaluation/Vanilla_Untagged/output_vanilla_untagged.jsonl" 
    ground_truth_file_path = "Data/test_150.jsonl"
    binary_labels, scores = parse_jsonl(output_file_path, ground_truth_file_path)
    print(binary_labels)
    print(" ---- ")
    print(scores)
    plot_roc_curve(binary_labels, scores)
