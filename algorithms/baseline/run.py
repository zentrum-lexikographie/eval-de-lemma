import sys
import json

sys.path.append("../..")
from src.loader import load_data
from src.run import run_algorithm
DATASETSPATH = "../../../lemma-data"
#DATASETSPATH = "../../datasets"

import warnings
warnings.filterwarnings("ignore")


def predict(x_test, y_test, z_test):
    # baseline lemmatization: lemma = token
    return x_test


# (A) Run all benchmarks
results = []

for x_test, y_test, z_test, dname in load_data(DATASETSPATH):
    try:
        results.append(run_algorithm(predict, x_test, y_test, z_test, dname,
                                     'baseline'))
    except Exception as err:
        print(err)


# store results
with open("../../nbs/results-baseline.json", "w") as fp:
    json.dump(results, fp, indent=4)
