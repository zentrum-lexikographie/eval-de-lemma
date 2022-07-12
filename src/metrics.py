# -*- coding: utf-8 -*-
from sklearn.metrics import (
    recall_score, precision_score, f1_score,
    accuracy_score, balanced_accuracy_score,
    cohen_kappa_score)
from typing import List
import numpy as np
from nltk.metrics import edit_distance


def log_levenshtein(y_true: List[str], y_pred: List[str]) -> float:
    """logarithmized Levenshtein distance"""
    N = len(y_true)
    # TODO default of substitution cost is 1, set to 2?? substitution = insert+delete
    loglev = sum(np.log(edit_distance(y_true[i], y_pred[i]) + 1)
                 for i in range(N)) / N
    return loglev    

def compute_metrics(y_true: List[str], y_pred: List[str]) -> dict:
    """
    compute different token-level and character-level metrics (Levenshtein distance)
    """
    res = {}
    return res

def metrics_by_pos(y_true: List[str], y_pred: List[str], z: List[str]) -> dict:
    """compute metrics by POS tag"""
    POS = set(z)
    for p in POS:
        compute_metrics(y_true, y_pred)


print(log_levenshtein(['ja', 'der'], ['ja', 'die']))
