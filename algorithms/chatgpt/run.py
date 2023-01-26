import json
import logging
import openai
import sys

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


openai.api_key = ""


def predict(x_test, y_test, z_test, z_test_xpos):
    lemmata = []
    for sent in x_test:
        prompt = f"Lemmatisiere bitte folgende Liste von Tokens: {sent}"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024
        )
        answer = response["choices"][0]["text"]
        # response structure:
        """["Ich", "bin", "ein", "Berliner"]

        Ich - ich
        bin - sein
        ein - ein
        Berliner - Berliner

        Please note that this lemmatization of this German text is based ..."""
        lemmata.append(line.split(' - ')[1] for line in
                       answer.split('\n\n')[1].split('\n'))
    return lemmata


# (A) Run all benchmarks
results = []

for x_test, y_test, z_test, z_test_xpos, dname in load_data(DATASETSPATH):
    try:
        results.append(run_algorithm(predict, x_test, y_test, z_test,
                                     z_test_xpos, dname, 'chatgpt'))
    except Exception as err:
        logger.error(err)


# store results
with open("../../nbs/results-chatgpt.json", "w") as fp:
    json.dump(results, fp, indent=4)
