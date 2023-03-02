# -*- coding: utf-8 -*-
import csv
import gc
import itertools
import json
import logging
import os
import sys

sys.path.append("../..")
from postprocess import clean_up
from src.loader import load_data
from src.metrics import metrics_by_pos


# logging settings
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="../../../logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s: %(message)s",
    datefmt="%y-%m-%d %H:%M:%S"
)

DATASETSPATH = "../../datasets"

import warnings
warnings.filterwarnings("ignore")


def predict(x_test, y_test, z_test, z_test_xpos, dname):
    """Read lemmata from API query outputs, resolve alignment issues."""
    lemmata, forms = clean_up(f'../../nbs/chatgpt_outputs/chatgpt-{dname}.txt')
    keep_sents = []  # indices of kept sentences in in gold data
    keep_sents_lem = []  # indices of kept sentences predicted lemma list
    wrong = dict()
    j = 0  # index in token list
    for i, sent in enumerate(lemmata):
        if i > len(x_test)-1 or j > len(x_test)-1:  # end of token list reached
            break
        if len(sent) != len(x_test[j]):
            # alignment issues:
            if len(sent) == len(x_test[j-1]):  # check previous
                keep_sents.append(j-1)
                keep_sents_lem.append(i)
                continue
            elif len(sent) == len(x_test[j+1]):  # check next
                keep_sents.append(j+1)
                keep_sents_lem.append(i)
                j += 2
                continue
            elif len(sent) == len(x_test[j+2]):  # check after next
                keep_sents.append(j+2)
                keep_sents_lem.append(i)
                j += 3
            elif len(sent) == len(x_test[j-2]):  # check before previous
                keep_sents.append(j-2)
                keep_sents_lem.append(i)
                j -= 1
            else:  # different sentence length
                wrong[str(i)] = (sent, x_test[j])
                j += 1
        else:
            keep_sents.append(j)
            keep_sents_lem.append(i)
            j += 1
    assert len(keep_sents) == len(keep_sents_lem)
    return forms, [lemmata[j] for j in keep_sents_lem], \
        [x_test[j] for j in keep_sents], [y_test[j] for j in keep_sents], \
        [z_test[j] for j in keep_sents], [z_test_xpos[j] for j in keep_sents]


# run all benchmarks
results = []
formats = []  # count different output formats

for x_test, y_test, z_test, z_test_xpos, dname in load_data(DATASETSPATH):
    try:  # not all datasets lemmatized with gpt-3
        if os.path.exists(f"../../nbs/chatgpt_outputs/chatgpt-{dname}.txt"):
            # create new lists with matching indices
            f, y_pred, x_test_eval, y_test_eval, z_test_eval, z_test_xpos_eval \
                = predict(x_test, y_test, z_test, z_test_xpos, dname)
            print(len(y_pred), len(x_test_eval))
            # number of ignored sentences
            num_ignored_sents = len(x_test) - len(y_pred)
            num_sents = len(x_test)
            # flatten sequences
            y_test_eval = list(itertools.chain(*y_test_eval))
            z_test_xpos_eval = list(itertools.chain(*z_test_xpos_eval))
            y_pred = list(itertools.chain(*y_pred))
            x_test_eval = list(itertools.chain(*x_test_eval))
            z_test_eval = list(itertools.chain(*z_test_eval))
            # store and output lemmatizations of first 2000 tokens
            df = []
            for i in range(len(y_pred)):
                # dataframe with token, upos tag, xpos tag, gold lemma, pred
                df.append([x_test_eval[i], z_test_eval[i], z_test_xpos_eval[i],
                           y_test_eval[i], y_pred[i]])
            with open(f"../../nbs/lemmata/{dname}/chatgpt-{dname}.csv", 'w',
                      newline='', encoding="utf-8") as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',')
                csvwriter.writerow(['token', 'tag', 'tag_STTS',
                                    'lemma_gold', 'lemma_pred'])
                csvwriter.writerows(df)
            # compute metrics, considering content words only, certain PoS tags
            metrics = metrics_by_pos(y_test_eval, y_pred, z_test_eval,
                                     z_test_xpos_eval)
            size = len(y_test_eval)
            # delete variables, collect garbage
            del x_test, y_test, y_pred, z_test, z_test_xpos
            del x_test_eval, y_test_eval, z_test_eval, z_test_xpos_eval
            gc.collect()
            results.append({
                'dataset': dname, 'sample-size': size,
                'lemmatizer': 'chatgpt', 'metrics': metrics,
                'memory_current': 0,
                'memory_peak': 0,
                'num_sents_corpus': num_sents,
                'num_sents_ignored': num_ignored_sents})
            formats[dname] = f
    except Exception as err:
        logger.error(err)


# store results
with open("../../nbs/results-chatgpt.json", "w") as fp:
    json.dump(results, fp, indent=4)

# store output formats
with open("../../nbs/chatgpt_outputs/formats.json", "w") as fp:
    json.dump(formats, fp, indent=4)
