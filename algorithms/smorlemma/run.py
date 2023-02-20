import itertools
import json
import logging
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

transducer = "zmorge-20150315-smor_newlemma.ca"

# uPoS tags and their SMOR equivalent
smor_tags = {'NOUN': 'NN', 'PROPN': 'NPROP', 'VERB': 'V', 'ADJ': 'ADJ',
             'ADV': 'ADV'}


def predict(x_test, y_test, z_test, z_test_xpos):
    """Predicts a lemma based on the SMORLemma analyses: If the gold lemma is
    among the predictions, it is returned. Otherwise the empty string is
    returned.
    """
    predicted = []
    for i, x in enumerate(list(itertools.chain(*x_test))):
        try:
            p = run(["fst-infl2", transducer], stdout=PIPE, input=x,
                    encoding='utf-8')
            # list of morphological analyses, first 2 elements are '>' and 'x'
            results = p.stdout.split()[2:]
            # list of lemmata
            lemmata = [re.sub(r'<[-#\+~]*[1-3A-Za-z]*>', '', r)
                       for r in results]
            if y_test[i] in lemmata:  # gold lemma in analyses
                predicted.append(y_test[i])
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
