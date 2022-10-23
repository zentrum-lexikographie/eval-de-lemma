import json
import sys
import trankit

sys.path.append("../..")
from src.loader import load_data
from src.run import run_algorithm

DATASETSPATH = "../../datasets"

import warnings
warnings.filterwarnings("ignore")


# (A) Load trankit model
model = trankit.Pipeline(lang='german', gpu=False)


def predict(x_test, y_test, z_test):
    lemmatized_doc = model.lemmatize(x_test)
    return [[t['lemma'] for t in sent['tokens']]
            for sent in lemmatized_doc['sentences']]


# (A) Run all benchmarks
results = []

for x_test, y_test, z_test, dname in load_data(DATASETSPATH):
    try:
        results.append(run_algorithm(predict, x_test, y_test, z_test, dname,
                                     'trankit'))
    except Exception as err:
        print(err)


# store results
with open("../../nbs/results-trankit.json", "w") as fp:
    json.dump(results, fp, indent=4)
