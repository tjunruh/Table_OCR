#!/usr/bin/env python3

"""
Implement automatic benchmarking given existing image and labels.
Usage see bboxtests/vanilla.py
"""

import csv
from datetime import datetime
from pathlib import Path
import sys
import warnings
warnings.filterwarnings("ignore")


def benchmark(str_true: str, str_pred: str) -> tuple[int, int, int]:
    """
    Perform benchmarking on prediction string against true string, where
        - True Positive is number of letters the prediction correctly matches
        - False Positive is number of letters the prediction incorrectly captures
        - False Negative is number of letters the prediction misses from truth
    and overall rules are
        - TP + FN = len(str_true)
        - TP + FP = len(str_pred)

    Args:
        str_true: ground truth string
        str_pred: prediction string

    Returns:
    (true_positive, false_positive, false_negative)
    """
    str_true = "".join(a for a in str_true if a.isalnum()).upper()
    str_pred = "".join(a for a in str_pred if a.isalnum()).upper()
    i_true, i_pred = 0, 0
    true_positive = 0
    while True:
        if i_true == len(str_true) or i_pred == len(str_pred):
            break
        ahead_true = str_true[i_true:]
        char_pred = str_pred[i_pred]
        i_find = ahead_true.find(char_pred)
        if i_find >= 0:
            i_true += 1 + i_find
            true_positive += 1
        i_pred += 1
    return true_positive, (len(str_pred) - true_positive), (len(str_true) - true_positive)

def test_benchmark():
    """
    This function is used to test the benchmark function under the PyTest
    framework
    """
    # capture all TP
    assert benchmark("abc", "abc") == (3, 0, 0)
    # ignore non-alphanumerical chars
    assert benchmark(",a/b$c*", "(a#b!c-]") == (3, 0, 0)
    # capture incorrect matches
    assert benchmark("abc", "adcc") == (2, 2, 1)
    # capture missing matches
    assert benchmark("1234", "153") == (2, 1, 2)
    # capture order also
    assert benchmark("aabbcc", "aaccbb") == (4, 2, 2)
    # idk
    assert benchmark("aabbcc", "bbc234") == (3, 3, 3)


def bboxbenchmark(predict_class, root_dir):
    """
    Benchmark on a directory of images with label file under `labels.csv`
    Args:
        predict_class: subclass of application.predict.predict
        root_dir: path to the image directory

    Returns:

    """
    root_dir = Path(root_dir).resolve()
    if not root_dir.is_dir():
        raise Exception(f"{root_dir} is not a directory")
    labels_file = root_dir / "labels.csv"
    if not labels_file.exists():
        raise FileNotFoundError("labels.csv not found")
    labels = {}
    with labels_file.open("r") as f:
        reader = csv.reader(f)
        for row in reader:
            labels[row[0]] = row[1]
    empty_labels = [k for k, v in labels.items() if not v]
    if empty_labels:
        raise Exception(
            f"{len(empty_labels)} image(s) are not labeled:\n{empty_labels}")
    p = predict_class()
    results = {}
    for img, label in labels.items():
        img_path = str(root_dir / img)
        pred = "".join(p.get_letters(img_path, 2)).lower()
        results[img] = [pred, *benchmark(label, pred)]
    result_file_name = predict_class.__name__ + "_" + str(
        datetime.now().strftime("%Y-%m-%d_%H:%M:%S")) + ".csv"
    with Path(root_dir / result_file_name).open("w+") as f:
        writer = csv.writer(f)
        writer.writerow(["image", "label", "prediction", "tp", "fp", "fn"])
        for img in results.keys():
            writer.writerow([img, labels[img], *results[img]])
    return result_file_name


def get_metrics(*csv_files: Path | str):
    from tabulate import tabulate
    tp, fp, fn = 0, 0, 0
    for csv_file in csv_files:
        csv_file = Path(csv_file).resolve()
        if not csv_file.is_file():
            raise FileNotFoundError(f"{csv_file} not exists")
        with csv_file.open("r") as f:
            reader = csv.reader(f)
            nrow = 0
            for row in reader:
                nrow += 1
                if len(row) < 6:
                    raise IndexError(f"Row #{nrow} does not have at least 6 columns")
                if nrow == 1:
                    continue
                tp += int(row[3])
                fp += int(row[4])
                fn += int(row[5])
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 / (1/precision + 1/recall)
    print(tabulate([
        ["Precision", precision],
        ["Recall", recall],
        ["F1 Score", f1]
    ], tablefmt="simple_grid"))

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        raise Exception("No files given")
    get_metrics(*args)