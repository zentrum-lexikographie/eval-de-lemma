# -*- coding: utf-8 -*-
import json
import logging
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


def predict(x_test, dname):
    """Read lemmata from API query outputs."""
    lemmata = clean_up(f'../../nbs/chatgpt_outputs/chatgpt-{dname}.txt')
    # TODO prevent index errors
    return lemmata


# run all benchmarks
results = []

for x_test, y_test, z_test, z_test_xpos, dname in load_data(DATASETSPATH):
    try:
        results.append(run_algorithm(predict, x_test, y_test, z_test,
                                     z_test_xpos, dname, 'chatgpt'))
    except Exception as err:
        logger.error(err)


# store results
with open("../../nbs/results-chatgpt.json", "w") as fp:
    json.dump(results, fp, indent=4)
