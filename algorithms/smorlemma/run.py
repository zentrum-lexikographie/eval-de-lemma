import collections
import json
import logging
import re
import sys

from subprocess import Popen, PIPE


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

transducer = "zmorge-20150315-smor_newlemma.ca"

def predict(x_test, y_test, z_test):
    predicted = []
    for x in x_test:
        process = Popen(["fst-infl2", transducer], stdin=PIPE, stdout=PIPE)
        stdout = process.communicate(input=x)[0]
        results = stdout.split()  # list of morphological analyses
        # list of lemmata
        lemmata = [re.sub('<[-#\+]*[A-Za-z]*>', '', r) for r in results]
        # return most frequent lemma
        predicted.append(collections.Counter(results).most_common()[0][0])
    return predicted


results = []

for x_test, y_test, z_test, z_test_xpos, dname in load_data(DATASETSPATH):
    try:
        results.append(run_algorithm(predict, x_test, y_test, z_test,
                                     z_test_xpos, dname, 'smorlemma'))
    except Exception as err:
        logger.error(err)


# store results
with open("../../nbs/results-smorlemma.json", "w") as fp:
    json.dump(results, fp, indent=4)
