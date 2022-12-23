import collections
import itertools
import json
import logging
import re
import sys

from subprocess import run, PIPE


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


def predict(x_test, y_test, z_test):
    """
    Predicts a lemma based on the SMORLemma analyses: If the gold lemma is
    among the predictions, it is returned. Otherwise the most frequent lemma
    with the gold PoS tag is returned or, if none of the analyses contains the
    gold PoS tag, simply the most frequent lemma is returned.

    Parameters
    ----------
    x_test : TYPE
        DESCRIPTION.
    y_test : TYPE
        DESCRIPTION.
    z_test : TYPE
        DESCRIPTION.

    Returns
    -------
    predicted : TYPE
        DESCRIPTION.

    """
    predicted = []
    for i, x in enumerate(list(itertools.chain(*x_test))):
        try:
            p = run(["fst-infl2", transducer], stdout=PIPE, input=x,
                    encoding='utf-8')
            # list of morphological analyses, first 2 elements are '>' and 'x'
            results = p.stdout.split()[2:]
            # list of lemmata
            lemmata = [re.sub(r'<[-#\+~]*[1-3A-Za-z]*>', '', r) for r in results]
            if y_test[i] in lemmata:  # gold lemma in analyses
                predicted.append(y_test[i])
            else:
                tag = smor_tags[z_test[i]]  # gold uPoS tag, converted to SMOR tag
                if f'<+{tag}>' in "".join(results):
                    # return most frequent lemma with gold PoS tag
                    lemmata = [re.sub(r'<[-#\+~]*[1-3A-Za-z]*>', '', r)
                               for r in results if f'<+{tag}>' in r]
                # return most frequent lemma
                predicted.append(collections.Counter(lemmata).most_common()[0][0])
        except Exception as err:
            logger.error(x, err)
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
