import json
import logging
import sys
import trankit

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


# (A) Load trankit model
model = trankit.Pipeline(lang='german', gpu=False)


def predict(x_test, y_test, z_test, z_test_xpos):
    lemmatized_doc = model.lemmatize(x_test)
    return [[t['lemma'] for t in sent['tokens']]
            for sent in lemmatized_doc['sentences']]


# (A) Run all benchmarks
results = []

for x_test, y_test, z_test, z_test_xpos, dname in load_data(DATASETSPATH):
    try:
        results.append(run_algorithm(predict, x_test, y_test, z_test,
                                     z_test_xpos, dname, 'trankit'))
    except Exception as err:
        logger.error(err)


# store results
with open("../../nbs/results-trankit.json", "w") as fp:
    json.dump(results, fp, indent=4)
