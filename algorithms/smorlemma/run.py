import itertools
import json
import logging
import os
import re
from subprocess import run, PIPE
import sys


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

# check if SMORLemma and files have been installed to correct directory
if os.path.isdir("../../SMORLemma"):
    os.system("mv ../../SMORLemma SMORLemma/")
    os.system("mv ../../zmorge-20150315.xml zmorge-20150315.xml")
    os.system("mv ../../zmorge-20150315-smor_newlemma.ca zmorge-20150315-smor_newlemma.ca")

transducer = "zmorge-20150315-smor_newlemma.ca"

# uPoS tags and their SMOR equivalent
smor_tags = {'NOUN': 'NN', 'PROPN': 'NPROP', 'VERB': 'V', 'ADJ': 'ADJ',
             'ADV': 'ADV'}


def predict(x_test, y_test, z_test, z_test_xpos, dname):
    """Predicts a lemma based on the SMORLemma analyses: If the gold lemma is
    among the predictions, it is returned. Otherwise the empty string is
    returned.
    """
    predicted = []
    y_flat = list(itertools.chain(*y_test))
    for i, x in enumerate(list(itertools.chain(*x_test))):
        try:
            p = run(["fst-infl2", transducer], stdout=PIPE, input=x,
                    encoding='utf-8')
            # list of morphological analyses, first 2 elements are '>' and 'x'
            results = p.stdout.split()[2:]
            # list of lemmata
            lemmata = [re.sub(r'<[-#\+~]*[1-3A-Za-z]*>', '', r)
                       for r in results]
            if y_flat[i] in lemmata:  # gold lemma in analyses
                predicted.append(y_flat[i])
            else:
                predicted.append('')
        except Exception as err:
            logger.error(x, err)
    return predicted


# run all benchmarks
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
