import logging
import json
import sys

import spacy

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

# instanciate SpaCy model
model = spacy.load('de_core_news_lg')
model.disable_pipes(["ner", "parser"])


def predict(x_test, y_test, z_test, z_test_xpos):
    """Performs lemmatization on a nested list of tokens using SpaCy2."""
    lemmatizer = model.pipeline[0][1]
    docs = [lemmatizer(spacy.tokens.doc.Doc(model.vocab, words=sequence))
            for sequence in x_test]
    return [[w.lemma_ for w in doc] for doc in docs]


# run all benchmarks
results = []

for x_test, y_test, z_test, z_test_xpos, dname in load_data(DATASETSPATH):
    try:
        results.append(run_algorithm(predict, x_test, y_test, z_test,
                                     z_test_xpos, dname, 'spacy2'))
    except Exception as err:
        logger.error(err)


# store results
with open("../../nbs/results-spacy2.json", "w") as fp:
    json.dump(results, fp, indent=4)
