import torch
from torcheval.metrics.functional import binary_f1_score
from sklearn.metrics import precision_score, recall_score
import json
from jaro import jaro_winkler_metric

def read_lines(file: str) -> list[str]:
    """Read lines from a file and return as a list."""
    with open(file, "r") as f:
        lines = f.readlines()
    return lines

def read_jsonl(file: str) -> list[list[tuple[str]]]:
    """Read JSON lines from a file and parse into a list of lists of tuples."""
    lines = read_lines(file)
    result = [[tuple(triplet) for triplet in json.loads(line)] for line in lines]
    return result

def read_txt(file: str) -> list[str]:
    """Read lines from a text file and return as a list."""
    return read_lines(file)

def to_binary(preds, gt):
    """Convert prediction and ground truth samples to binary classification."""
    max_len = max(len(preds), len(gt))
    output = [1 if pred in gt else 0 for pred in preds]
    target = [1 if gt in preds else 0 for gt in gt]

    # Pad the shorter tensor with zeros
    if len(output) < max_len:
        output.extend([0] * (max_len - len(output)))
    if len(target) < max_len:
        target.extend([0] * (max_len - len(target)))

    return torch.tensor(output), torch.tensor(target)

def calculate_scores(preds, gt):
    """Calculate F1 score, precision, recall, and Jaro-Winkler score."""
    max_len = max(len(gt), len(preds))
    f1_score_sum = precision_sum = recall_sum = jw_score_sum = 0

    for i in range(max_len):
        # Calculate F1 score, precision, and recall
        pred_sample = preds[min(i, len(preds) - 1)]
        gt_sample = gt[min(i, len(gt) - 1)]
        output, target = to_binary(pred_sample, gt_sample)
        output, target = torch.tensor(output), torch.tensor(target)
        f1_score_sum += binary_f1_score(output, target)
        precision_sum += precision_score(target, output)
        recall_sum += recall_score(target, output)

        # Calculate Jaro-Winkler score
        pred_sample_txt = ' '.join([' '.join(triplet) for triplet in pred_sample])
        gt_sample_txt = ' '.join([' '.join(triplet) for triplet in gt_sample])
        jw_score_sum += jaro_winkler_metric(pred_sample_txt, gt_sample_txt)

    # Calculate averages
    f1_score = f1_score_sum / max_len
    precision = precision_sum / max_len
    recall = recall_sum / max_len
    jw_score = jw_score_sum / max_len

    return float(f1_score), precision, recall, jw_score

if __name__ == "__main__":
    # Read predictions and ground truth
    preds = read_jsonl("Evaluation/preds.jsonl")
    gt = read_jsonl("Evaluation/gt.jsonl")

    print(f"GT: {gt}")
    print(f"Preds: {preds}")

    # Calculate scores
    f1_score, precision, recall, jw_score = calculate_scores(preds, gt)

    # Print scores
    print("F1 Score:", f1_score)
    print("Precision:", precision)
    print("Recall:", recall)
    print("Jaro-Winkler Score:", jw_score)
