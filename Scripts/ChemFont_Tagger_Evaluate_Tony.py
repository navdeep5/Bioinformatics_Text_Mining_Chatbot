import torch
from torcheval.metrics.functional import binary_f1_score, binary_precision, binary_recall
import json
from jaro import jaro_winkler_metric
from sklearn.metrics import roc_curve, roc_auc_score

import numpy as np
import matplotlib.pyplot as plt

from pprint import pprint
def read_io_jsonl(preds_file: str, gt_file: str) -> list[list[tuple[str]]]:
    '''Reads a jsonl file with input and output format and
    returns a list of lists of triplets'''

    # Read the predictions and ground truth files
    with open(preds_file, "r") as f:
        preds_lines: list[str] = f.readlines()
    with open(gt_file, "r") as f:
        gt_lines: list[str] = f.readlines()
    
    # Get the ground truth
    gt = []
    for gt_sample in gt_lines:
        gt.append([tuple(triplet) for triplet in json.loads(gt_sample)["output"]])

    # parsed preds will contain either:
    # 1. a list of triplets
    # 2. an empty list
    parsed_preds = []  # len = 150 (number of samples)
    failed = 0  # counter for failed samples

    # Parse the predictions
    for sample in preds_lines:
        # try to fix the sample (prediction) before reading it
        sample = sample.replace("\"[[", "[[")
        sample = sample.replace("]]\"", "]]")
        sample = sample.replace("\'", "\"")

        # try to read the sample (prediction)
        try:
            out = json.loads(sample)["output"]

            # check if Nav said the output is valid
            if not json.loads(sample)["valid"]:
                raise Exception("Invalid output")  # raise an exception to jump to except block
            
            # add triplets to parsed_preds
            parsed_preds.append([tuple(triplet) for triplet in out])
        
        # if the sample (prediction) is not valid, add an empty list to parsed_preds
        except Exception as e:
            failed += 1
            # print(e)
            parsed_preds.append([])

    return parsed_preds, gt, failed

def read_txt(file: str) -> list[str]:
    with open(file, "r") as f:
        lines = f.readlines()
    return lines

def to_binary(preds: list[tuple], gt: list[tuple]) -> tuple[list[int], list[int]]:
    gt = set(gt)
    output = []
    target = []
    for pred in preds:
        if pred in gt:
            # real triplet (true positive)
            gt.remove(pred)
            target.append(1)
        else:
            # fake triplet (false positive)
            target.append(0)

        # positive
        output.append(1)

    # unextracted triplets (false negatives)
    target.extend([1 for item in gt])
    output.extend([0 for item in gt])

    return output, target

def f1(preds: list[list[tuple[str]]], gt: list[list[tuple[str]]]) -> list:
    N = len(gt)
    scores = []

    for i in range(N):
        # print("preds", preds[i])
        # print("gt", gt[i])
        output, target = to_binary(preds[i], gt[i])
        output, target = torch.tensor(output), torch.tensor(target)
        # print("out", output)
        # print("target", target)
        scores.append(binary_f1_score(output, target))

    return scores

def precision(preds: list[list[tuple[str]]], gt: list[list[tuple[str]]]) -> list:
    N = len(gt)
    scores = []

    for i in range(N):
        output, target = to_binary(preds[i], gt[i])
        output, target = torch.tensor(output), torch.tensor(target)
        scores.append(binary_precision(output, target))

    return scores

def recall(preds: list[list[tuple[str]]], gt: list[list[tuple[str]]]) -> list:
    N = len(gt)
    scores = []

    for i in range(N):
        output, target = to_binary(preds[i], gt[i])
        output, target = torch.tensor(output), torch.tensor(target)
        scores.append(binary_recall(output, target))

    return scores

def jaro_winkler(preds: list[list[tuple[str]]], gt: list[list[tuple[str]]]) -> list:
    N = len(gt)
    scores = []

    for i in range(N):
        output = json.dumps(preds[i])
        target = json.dumps(gt[i])
        scores.append(jaro_winkler_metric(output, target))

    return scores

def roc(preds, gt, title=""):
    y_true = []
    y_score = []
    for i in range(len(gt)):
        # Collect data for ROC Curve
        output, target = to_binary(preds[i], gt[i])
        # rescale output 1's to between 1 and 0 with value at the beginning with higher scores (confidence)
        output = torch.tensor(output)
        output = output / torch.arange(1, output.shape[0] + 1)

        y_true.extend(target)
        y_score.extend(output.tolist())

    # print(y_score)
    fpr, tpr, threshold = roc_curve(y_true, y_score)
    roc_auc = roc_auc_score(y_true, y_score)

    # print(f"{len(fpr)=}")  # sanity check for roc_curve (make sure len(fpr) >> 1)
    # # Plot ROC Curve
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    # plt.xlim([0.0, 1.0])
    # plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(title + " " + 'ROC Curve')
    plt.legend(loc="lower right")
    plt.show()
    # plt.savefig(f"figs/roc_{title}.png")

if __name__ == "__main__":
    gt_file = "Data/test_150.jsonl"
    tag_tag = "Evaluation/TaggedVanilla_Tagged/output_taggedVanilla_tagged.jsonl"
    tag_untag = "Evaluation/TaggedVanilla_Untagged/output_taggedVanilla_untagged.jsonl"
    van_tag = "Evaluation/Vanilla_Tagged/output_vanilla_tagged.jsonl"
    van_untag = "Evaluation/Vanilla_Untagged/output_vanilla_untagged.jsonl"

    ############################################################################################################
    print(f"{'Tag Tag':-^20}")
    preds, gt, failed = read_io_jsonl(tag_tag, gt_file)
    print(failed, "failed")  # logging the number of failed samples

    # f1, precision, recall
    f1_scores = f1(preds, gt)
    p_scores = precision(preds, gt)
    r_scores = recall(preds, gt)
    row = "{:<15} {:>10.3f} {:>10.3f} {:>10.3f} {:>10.3f}"
    print(f'{"Metric":<15} {"Mean":>10} {"STD":>10} {"Max":>10} {"Min":>10}')
    print(row.format("F1", np.mean(f1_scores), np.std(f1_scores), np.max(f1_scores), np.min(f1_scores)))
    print(row.format("Precision", np.mean(p_scores), np.std(p_scores), np.max(p_scores), np.min(p_scores)))
    print(row.format("Recall", np.mean(r_scores), np.std(r_scores), np.max(r_scores), np.min(r_scores)))
    # jaro-winkler
    jaro_scores = jaro_winkler(preds, gt)
    print(row.format("Jaro-Winkler", np.mean(jaro_scores), np.std(jaro_scores), np.max(jaro_scores), np.min(jaro_scores)))
    roc(preds, gt, title="Tag-Train Tag-Data")

    ############################################################################################################
    print(f"{'Tag Untag':-^20}")
    preds, gt, failed = read_io_jsonl(tag_untag, gt_file)
    print(failed, "failed")  # logging the number of failed samples

    # f1, precision, recall
    f1_scores = f1(preds, gt)
    p_scores = precision(preds, gt)
    r_scores = recall(preds, gt)
    row = "{:<15} {:>10.3f} {:>10.3f} {:>10.3f} {:>10.3f}"
    print(f'{"Metric":<15} {"Mean":>10} {"STD":>10} {"Max":>10} {"Min":>10}')
    print(row.format("F1", np.mean(f1_scores), np.std(f1_scores), np.max(f1_scores), np.min(f1_scores)))
    print(row.format("Precision", np.mean(p_scores), np.std(p_scores), np.max(p_scores), np.min(p_scores)))
    print(row.format("Recall", np.mean(r_scores), np.std(r_scores), np.max(r_scores), np.min(r_scores)))
    # jaro-winkler
    jaro_scores = jaro_winkler(preds, gt)
    print(row.format("Jaro-Winkler", np.mean(jaro_scores), np.std(jaro_scores), np.max(jaro_scores), np.min(jaro_scores)))
    roc(preds, gt, title="Tag-Train Untag-Data")

    ############################################################################################################
    print(f"{'Van Tag':-^20}")
    preds, gt, failed = read_io_jsonl(van_tag, gt_file)
    print(failed, "failed")  # logging the number of failed samples

    # f1, precision, recall
    f1_scores = f1(preds, gt)
    p_scores = precision(preds, gt)
    r_scores = recall(preds, gt)
    row = "{:<15} {:>10.3f} {:>10.3f} {:>10.3f} {:>10.3f}"
    print(f'{"Metric":<15} {"Mean":>10} {"STD":>10} {"Max":>10} {"Min":>10}')
    print(row.format("F1", np.mean(f1_scores), np.std(f1_scores), np.max(f1_scores), np.min(f1_scores)))
    print(row.format("Precision", np.mean(p_scores), np.std(p_scores), np.max(p_scores), np.min(p_scores)))
    print(row.format("Recall", np.mean(r_scores), np.std(r_scores), np.max(r_scores), np.min(r_scores)))
    # jaro-winkler
    jaro_scores = jaro_winkler(preds, gt)
    print(row.format("Jaro-Winkler", np.mean(jaro_scores), np.std(jaro_scores), np.max(jaro_scores), np.min(jaro_scores)))
    roc(preds, gt, title="Untag-Train Tag-Data")

    ############################################################################################################
    print(f"{'Van Untag':-^20}")
    preds, gt, failed = read_io_jsonl(van_untag, gt_file)
    print(failed, "failed")  # logging the number of failed samples

    # f1, precision, recall
    f1_scores = f1(preds, gt)
    p_scores = precision(preds, gt)
    r_scores = recall(preds, gt)
    row = "{:<15} {:>10.3f} {:>10.3f} {:>10.3f} {:>10.3f}"
    print(f'{"Metric":<15} {"Mean":>10} {"STD":>10} {"Max":>10} {"Min":>10}')
    print(row.format("F1", np.mean(f1_scores), np.std(f1_scores), np.max(f1_scores), np.min(f1_scores)))
    print(row.format("Precision", np.mean(p_scores), np.std(p_scores), np.max(p_scores), np.min(p_scores)))
    print(row.format("Recall", np.mean(r_scores), np.std(r_scores), np.max(r_scores), np.min(r_scores)))
    # jaro-winkler
    jaro_scores = jaro_winkler(preds, gt)
    print(row.format("Jaro-Winkler", np.mean(jaro_scores), np.std(jaro_scores), np.max(jaro_scores), np.min(jaro_scores)))
    roc(preds, gt, title="Untag-Train Untag-Data")