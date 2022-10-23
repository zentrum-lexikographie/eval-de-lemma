import simplemma
import sys
import json

sys.path.append("../..")
from src.loader import load_data
from src.run import run_algorithm


DATASETSPATH = "../../datasets"

import warnings
warnings.filterwarnings("ignore")


def predict(x_test, y_test, z_test):
    return [[simplemma.lemmatize(t, lang='de') for t in sent]
            for sent in x_test]


# (A) Run all benchmarks
results = []

for x_test, y_test, z_test, dname in load_data(DATASETSPATH):
    try:
        results.append(run_algorithm(predict, x_test, y_test, z_test, dname,
                                     'simplemma'))
    except Exception as err:
        print(err)


# store results
with open("../../nbs/results-simplemma.json", "w") as fp:
    json.dump(results, fp, indent=4)
