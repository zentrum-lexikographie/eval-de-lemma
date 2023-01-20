import json
import logging
import os
import pandas as pd
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


def predict(x_test, y_test, z_test, z_test_xpos):
    # write tokens to file
    with open("pretokenized.txt", "w") as fp:
        for sent in x_test:
            for token in sent:
                fp.write(token + '\n')
    # call rnn tagger without tokenization and pos tagging
    # pos tags
    os.system("cd RNNTagger && python3 './PyRNN/rnn-annotate.py' './lib/PyRNN/german' ../pretokenized.txt > ../tagged.txt")
    # reformatting
    os.system("cd RNNTagger && perl './scripts/reformat.pl' ../tagged.txt > ../reformatted.txt")
    # lemmatizer with NMT
    os.system("cd RNNTagger && python3 './PyNMT/nmt-translate.py' --print_source './lib/PyNMT/german' ../reformatted.txt > ../lemmatized.txt")
    # look-up
    os.system("cd RNNTagger && './scripts/lemma-lookup.pl' ../lemmatized.txt ../tagged.txt > ../output.tsv")
    output = pd.read_csv('tagged.tsv', sep='\t')  # lines: token, pos, lemma
    # delete temporary files
    #os.system("rm pretokenized.txt tag*.txt tagged.tsv")
    return output[2].to_list()


# (A) Run all benchmarks
results = []

for x_test, y_test, z_test, z_test_xpos, dname in load_data(DATASETSPATH):
    try:
        results.append(run_algorithm(predict, x_test, y_test, z_test,
                                     z_test_xpos, dname, 'rnntagger'))
    except Exception as err:
        logger.error(err)


# store results
with open("../../nbs/results-rnntagger.json", "w") as fp:
    json.dump(results, fp, indent=4)