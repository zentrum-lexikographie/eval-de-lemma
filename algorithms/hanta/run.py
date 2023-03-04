import json
import logging
import sys

from HanTa import HanoverTagger as ht

sys.path.append("../..")
from src.loader import load_data
from src.run import run_algorithm


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


tagger = ht.HanoverTagger('morphmodel_ger.pgz')


def predict(x_test, y_test, z_test, z_test_xpos, dname):
    """Performs lemmatization on a nested list of tokens using HanTa."""
    lemmata = []
    for j, sent in enumerate(x_test):  # lemmatize by sentence
        lemmata += [[tagger.analyze(token, taglevel=1)[0]
                    for i, token in enumerate(sent)]]
    return lemmata


# 1. run all benchmarks
results = []

for x_test, y_test, z_test, z_test_xpos, dname in load_data(DATASETSPATH):
    try:
        results.append(run_algorithm(predict, x_test, y_test, z_test,
                                     z_test_xpos, dname, 'hanta'))
    except Exception as err:
        logger.error(err)


# store results
with open("../../nbs/results-hanta.json", "w") as fp:
    json.dump(results, fp, indent=4)


# 2. run with PoS tags in input
def predict(x_test, y_test, z_test, z_test_xpos):
    """Performs lemmatization on a PoS-tagged list of tokens using HanTa."""
    lemmata = []
    for j, sent in enumerate(x_test):  # lemmatize by sentence
        lemmata += [[tagger.analyze(token, taglevel=1,
                                    pos=z_test_xpos[j][i])[0]
                    for i, token in enumerate(sent)]]
    return lemmata


results = []

for x_test, y_test, z_test, z_test_xpos, dname in load_data(DATASETSPATH):
    try:
        results.append(run_algorithm(predict, x_test, y_test, z_test,
                                     z_test_xpos, dname, 'hanta-pretagged'))
    except Exception as err:
        logger.error(err)


# store results
with open("../../nbs/results-hanta-pretagged.json", "w") as fp:
    json.dump(results, fp, indent=4)
