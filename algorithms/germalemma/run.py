import itertools
import json
import logging
import sys

from germalemma import GermaLemma

sys.path.append("../..")
from src.loader import load_data
from src.run import run_algorithm


# logging settings
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="../../logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s: %(message)s",
    datefmt="%y-%m-%d %H:%M:%S"
)

DATASETSPATH = "../../datasets"

import warnings
warnings.filterwarnings("ignore")


# instanciate lemmatizer, pass to function
lemmatizer = GermaLemma()


def lemmatize(token, pos):
    """predict a lemma given token and PoS tag"""
    try:
        return lemmatizer.find_lemma(token, pos)
    except Exception:
        # PoS tag not included
        return ""


def predict(x_test, y_test, z_test, z_test_xpos):
    """Lemmatize a flat list of tokens with GermaLemma."""
    return [lemmatize(x_test[i], z_test[i]) for i in range(len(x_test))]


# run all benchmarks
results = []

for x_test, y_test, z_test, z_test_xpos, dname in load_data(DATASETSPATH):
    try:
        # encode labels and flatten sequences
        x_test = list(itertools.chain(*x_test))
        z_test = list(itertools.chain(*z_test))
        results.append(run_algorithm(predict, x_test, y_test, z_test,
                                     z_test_xpos, dname, 'germalemma'))
    except Exception as err:
        logger.error(err)


# store results
with open("../../nbs/results-germalemma.json", "w") as fp:
    json.dump(results, fp, indent=4)
