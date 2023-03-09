# -*- coding: utf-8 -*-
import csv
import gc
import itertools
import json
import logging
import os
import sys

import datasketch
import kshingle as ks

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
    lemmata, forms = clean_up(f'../../nbs/gpt3_outputs/gpt3-{dname}.txt')
    keep_sents = []  # indices of kept sentences in in gold data
    keep_sents_lem = []  # indices of kept sentences predicted lemma list
    wrong = dict()
    print(f'{len(x_test)} sentences in data, {len(lemmata)} sentences in outputs')
    # initialize MinHash LSH Forest
    forest = datasketch.MinHashLSHForest(num_perm=128)
    # add all gpt3 sentences to forest
    for i, sent in enumerate(lemmata):
        s1 = ks.shingleset_k(' '.join(sent), k=5)
        varname = f'm{i}'
        locals()[varname] = datasketch.MinHash(num_perm=128)
        for s in s1:
            locals()[varname].update(s.encode('utf8'))
        forest.add(f"m{i}", locals()[varname])
    forest.index()
    # iterate gold sentences
    for i, sent in enumerate(y_test):
        sq = ks.shingleset_k(' '.join(sent), k=5)
        mq = datasketch.MinHash(num_perm=128)
        for s in sq:
            mq.update(s.encode('utf8'))
        try:  # check top 2
            result1, result2 = forest.query(mq, 2)  # highest similarity
            # top 1 result
            i_lem1 = int(result1.split('m')[1])  # index in predictions
            s_lem1 = lemmata[i_lem1]  # pred sentence
            # top 2 result
            i_lem2 = int(result2.split('m')[1])  # index in predictions
            s_lem2 = lemmata[i_lem2]  # pred sentence
            # check sentence lengths and jaccard similarities
            if len(s_lem1) == len(sent) and ks.jaccard_strings(
                    ' '.join(s_lem1), ' '.join(sent), k=5) > 0.3:
                keep_sents.append(i)
                keep_sents_lem.append(i_lem1)
            elif len(s_lem2) == len(sent) and ks.jaccard_strings(
                    ' '.join(s_lem2), ' '.join(sent), k=5) > 0.3:
                keep_sents.append(i)
                keep_sents_lem.append(i_lem2)
            else:
                wrong[str(i)] = (sent, s_lem1, s_lem2)
        except Exception:  # only top 1
            result1 = forest.query(mq, 1)  # highest similarity
            if result1:  # top 1 result
                i_lem1 = int(result1[0].split('m')[1])  # index in predictions
                s_lem1 = lemmata[i_lem1]  # pred sentence
                if len(s_lem1) == len(sent) and ks.jaccard_strings(
                        ' '.join(s_lem1), ' '.join(sent), k=5) > 0.3:
                    keep_sents.append(i)
                    keep_sents_lem.append(i_lem1)
                else:
                    wrong[str(i)] = (sent, s_lem1)
    return forms, [lemmata[j] for j in keep_sents_lem], \
        [x_test[j] for j in keep_sents], [y_test[j] for j in keep_sents], \
        [z_test[j] for j in keep_sents], [z_test_xpos[j] for j in keep_sents]


# run all benchmarks
results = []
formats = []  # count different output formats

for x_test, y_test, z_test, z_test_xpos, dname in load_data(DATASETSPATH):
    try:
        if os.path.exists(f"../../nbs/gpt3_outputs/gpt3-{dname}.txt"):
            # not all datasets lemmatized with gpt-3
            # create new lists with matching indices
            f, y_pred, x_test_eval, y_test_eval, z_test_eval, z_test_xpos_eval \
                = predict(x_test, y_test, z_test, z_test_xpos, dname)
            print(f'{len(y_pred)} sentences predicted.')
            # number of ignored sentences
            num_ignored_sents = len(x_test) - len(y_pred)
            num_sents = len(x_test)
            # flatten sequences
            y_test_eval = list(itertools.chain(*y_test_eval))
            z_test_xpos_eval = list(itertools.chain(*z_test_xpos_eval))
            y_pred = list(itertools.chain(*y_pred))
            x_test_eval = list(itertools.chain(*x_test_eval))
            z_test_eval = list(itertools.chain(*z_test_eval))
            # store and output lemmatizations tokens
            df = []
            for i in range(len(y_pred)):
                # dataframe with token, upos tag, xpos tag, gold lemma, pred
                df.append([x_test_eval[i], z_test_eval[i], z_test_xpos_eval[i],
                           y_test_eval[i], y_pred[i]])
            with open(f"../../nbs/lemmata/{dname}/gpt3-{dname}.csv", 'w',
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
                'lemmatizer': 'gpt3', 'metrics': metrics,
                'memory_current': 0,
                'memory_peak': 0,
                'num_sents_corpus': num_sents,
                'num_sents_ignored': num_ignored_sents})
            f['dataset'] = dname
            formats.append(f)
    except Exception as e:
        logger.error(e)


# store results
with open("../../nbs/results-gpt3.json", "w") as fp:
    json.dump(results, fp, indent=4)

# store output formats
with open("../../nbs/gpt3_outputs/formats.json", "w") as fp:
    json.dump(formats, fp, indent=4)
