# -*- coding: utf-8 -*-
from sklearn.metrics import (
    recall_score, precision_score, f1_score,
    accuracy_score, balanced_accuracy_score)
from typing import List, Set
import logging
import numpy as np
import pandas as pd
from nltk.metrics import edit_distance

# logging settings
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="../logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s: %(message)s",
    datefmt="%y-%m-%d %H:%M:%S"
)


def log_levenshtein(y_true: List[str], y_pred: List[str], sub: int = 1) -> float:
    """logarithmized Levenshtein distance
    sub: substitution cost, default 1, else 2 substitution = insert+delete"""
    N = len(y_true)
    try:
        loglev = sum(np.log(edit_distance(y_true[i], y_pred[i],
                                          substitution_cost=sub) + 1)
                     for i in range(N)) / N
        return loglev
    except Exception as e:
        logger.error(e)


def levenshtein(y_true: List[str], y_pred: List[str]) -> float:
    """average Levenshtein distance"""
    N = len(y_true)
    try:
        lev = sum((edit_distance(y_true[i], y_pred[i]))
                  for i in range(N)) / N
        return lev
    except Exception as e:
        logger.error(e)


def levenshtein_wordlen(y_true: List[str], y_pred: List[str]) -> float:
    """average Levenshtein distance normalized by word length"""
    N = len(y_true)
    try:
        lev = sum((edit_distance(y_true[i], y_pred[i])/len(y_true[i]))
                  for i in range(N)) / N
        return lev
    except Exception as e:
        logger.error(e)


def compute_metrics(y_true: List[str], y_pred: List[str]) -> dict:
    """
    compute different token-level and character-level metrics
    """
    res = {}
    res['number_of_lemmata'] = len(y_true)

    try:
        res['accuracy'] = accuracy_score(y_true, y_pred, normalize=True)
    except Exception as e:
        logger.error(e)

    try:
        res['recall'] = recall_score(y_true, y_pred, average='macro',
                                     zero_division=0)
    except Exception as e:
        logger.error(e)

    try:
        res['precision'] = precision_score(y_true, y_pred, average='macro',
                                           zero_division=0)
    except Exception as e:
        logger.error(e)

    try:
        res['f1'] = f1_score(y_true, y_pred, average='macro', zero_division=0)
    except Exception as e:
        logger.error(e)

    try:
        res['adj_recall'] = recall_score(y_true, y_pred, average='macro',
                                         zero_division=0)
    except Exception as e:
        logger.error(e)

    try:
        res['adj_precision'] = precision_score(y_true, y_pred, average='macro',
                                               zero_division=0)
    except Exception as e:
        logger.error(e)

    try:
        res['adj_f1'] = f1_score(y_true, y_pred, average='macro',
                                 zero_division=0)
    except Exception as e:
        logger.error(e)

    try:
        res['adj_accuracy'] = balanced_accuracy_score(y_true, y_pred,
                                                      adjusted=True)
    except Exception as e:
        logger.error(e)

    res['log-levenshtein'] = log_levenshtein(y_true, y_pred)
    res['log-levenshtein2'] = log_levenshtein(y_true, y_pred, sub=2)
    res['levenshtein'] = levenshtein(y_true, y_pred)
    res['levenshtein-wordlen'] = levenshtein_wordlen(y_true, y_pred)
    return res


def metrics_by_pos(y_true: List[str], y_pred: List[str], z: List[str],
                   POS: Set[str] = {'ADJ', 'ADV', 'NOUN', 'PROPN', 'VERB'})\
                    -> dict:
    """compute metrics by POS tag"""
    res = {}
    data = pd.DataFrame({'y_true': y_true, 'y_pred': y_pred, 'PoS': z})
    data_content = data[data['PoS'].isin(POS)]  # content words only
    # ignore POS tags other than content words for overall metrics
    res['overall'] = compute_metrics(data_content.y_true.tolist(),
                                     data_content.y_pred.tolist())
    for p in POS:  # metrics per PoS tag
        p_entries = data_content[data_content['PoS'] == p]
        res[p] = compute_metrics(p_entries.y_true.tolist(),
                                 p_entries.y_pred.tolist())
    return res


def demo():
    y1 = ['das', 'der', 'die']
    y2 = ['das', 'der', 'der']
    print(log_levenshtein(y1, y2), levenshtein(y1, y2),
          levenshtein_wordlen(y1, y2))


if __name__ == '__main__':
    demo()
