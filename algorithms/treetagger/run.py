import json
import logging
import sys
import treetaggerwrapper

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


tagger = treetaggerwrapper.TreeTagger(TAGLANG='de', TAGDIR='tagger/')


def predict(x_test, y_test, z_test):
    lemmata = []
    for sent in x_test:
        tags = tagger.tag_text(" ".join(sent))
        # saved as strings e.g. 'tiefe\tADJA\ttief'
        if len(tags) != len(sent):  # treetagger tokenization may be different
            # only tags until end of sentence length are appended
            lemmata.append([entry.split('\t')[2] if entry and len(entry.split('\t')) >= 3 else "" for entry in tags[:len(sent)]])
        else:
            lemmata.append([entry.split('\t')[2] if entry and len(entry.split('\t')) >= 3 else "" for entry in tags])
    return lemmata


# (A) Run all benchmarks
results = []

for x_test, y_test, z_test, z_test_xpos, dname in load_data(DATASETSPATH):
    try:
        results.append(run_algorithm(predict, x_test, y_test, z_test,
                                     z_test_xpos, dname, 'treetagger'))
    except Exception as err:
        logger.error(err)


# store results
with open("../../nbs/results-treetagger.json", "w") as fp:
    json.dump(results, fp, indent=4)
