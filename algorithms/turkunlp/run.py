import json
import logging
import os
import sys

import conllu

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


def predict(x_test, y_test, z_test, z_test_xpos):
    """Performs lemmatization on a list of tokens with Universal Lemmatizer."""
    # write tokens to txt file
    with open("tmp.txt", "w", encoding="utf-8") as f:
        for sent in x_test:  # one sentence per line
            f.write(" ".join(sent) + "\n")  # tokens separeted by white space
    # call lemmatizer
    os.system("cd Turku-neural-parser-pipeline && cat ../tmp.txt | python3 full_pipeline_stream.py --gpu -1 --conf models_de_gsd/pipelines.yaml parse_wslines > ../tmp.conllu")
    # read output file
    with open("tmp.conllu", 'r', encoding='utf-8') as fp:
        output = conllu.parse(fp.read())
    lemmata = [[tok['lemma'] for tok in sent] for sent in output]
    # remove temporary files
    os.system("rm tmp.*")
    return lemmata


# run all benchmarks
results = []

for x_test, y_test, z_test, z_test_xpos, dname in load_data(DATASETSPATH):
    try:
        results.append(run_algorithm(predict, x_test, y_test, z_test,
                                     z_test_xpos, dname, 'turkunlp'))
    except Exception as err:
        logger.error(err)


# store results
with open("../../nbs/results-turkunlp.json", "w") as fp:
    json.dump(results, fp, indent=4)
