# -*- coding: utf-8 -*-
from sklearn.metrics import (
    recall_score, precision_score, f1_score,
    accuracy_score, balanced_accuracy_score,
    cohen_kappa_score)
from typing import List, Set
import numpy as np
import pandas as pd
from nltk.metrics import edit_distance


def log_levenshtein(y_true: List[str], y_pred: List[str]) -> float:
    """logarithmized Levenshtein distance"""
    N = len(y_true)
    # TODO default of substitution cost is 1, set to 2?? substitution = insert+delete
    try:
        loglev = sum(np.log(edit_distance(y_true[i], y_pred[i]) + 1)
                 for i in range(N)) / N
        return loglev
    except Exception as e:
        print("cannot compute 'log-levenshtein': ", e)


def compute_metrics(y_true: List[str], y_pred: List[str]) -> dict:
    """
    compute different token-level and character-level metrics (Levenshtein distance)
    """
    res = {}
    res['number_of_lemmata'] = len(y_true)
    try:
        res['recall'] = recall_score(y_true, y_pred, average='micro', zero_division=0)
    except Exception as e:
        print("cannot compute 'recall': ", e)

    res['log-levenshtein'] = log_levenshtein(y_true, y_pred)
    return res

def metrics_by_pos(y_true: List[str], y_pred: List[str], z: List[str],
                   POS: Set[str]={'ADJ', 'ADV', 'NOUN', 'PROPN', 'VERB'})\
                    -> dict:
    """compute metrics by POS tag"""
    res = {}
    data = pd.DataFrame({'y_true': y_true, 'y_pred': y_pred, 'PoS': z})
    data_content = data[data['PoS'].isin(POS)]  # content words only
    res['overall'] = compute_metrics(data_content.y_true.tolist(),
                               data_content.y_pred.tolist())  # overall metrics
    for p in POS:  # metrics per PoS tag
        p_entries = data_content[data_content['PoS']==p]
        res[p] = compute_metrics(p_entries.y_true.tolist(),
                                   p_entries.y_pred.tolist())
    return res
