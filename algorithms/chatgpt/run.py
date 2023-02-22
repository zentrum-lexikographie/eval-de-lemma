# -*- coding: utf-8 -*-
import json
import logging
import os
import sys

sys.path.append("../..")
from src.loader import load_data
from src.run import run_algorithm
from postprocess import clean_up


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
    """Read lemmata from API query outputs."""
    lemmata = clean_up(f'../../nbs/chatgpt_outputs/chatgpt-{dname}.txt')
    # TODO prevent index errors
    print(len(x_test), len(lemmata))
    wrong = dict()
    j = 0  # second index for removals
    x_test2 = x_test
    for i, sent in enumerate(x_test2):
        print(j, i)
        if j > len(lemmata)-1:  # end of predicted list reached
            break
        if len(sent) != len(lemmata[j]):
            #print(sent, x_test[i])
            wrong[str(j)] = (sent, lemmata[j])
            # ignore sentence, remove from all arrays to ensure computations
            del lemmata[j], x_test[j], y_test[j], z_test[j], z_test_xpos[j]
        else:
            j += 1
    print(wrong)
    print(len(wrong.items()))
    return lemmata


# run all benchmarks
results = []

for x_test, y_test, z_test, z_test_xpos, dname in load_data(DATASETSPATH):
    try:  # not all datasets lemmatized with gpt-3
        if os.path.exists(f"../../nbs/chatgpt_outputs/chatgpt-{dname}.txt"):
            results.append(run_algorithm(predict, x_test, y_test, z_test,
                                         z_test_xpos, dname, 'chatgpt'))
    except Exception as err:
        logger.error(err)


# store results
with open("../../nbs/results-chatgpt.json", "w") as fp:
    json.dump(results, fp, indent=4)
