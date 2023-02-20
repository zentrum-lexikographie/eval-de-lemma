import json
import logging
import os
import sys
import time

import openai

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


# bash command: export OPEN_AI_KEY=INSERT_KEY_HERE
openai.api_key = os.environ["OPEN_AI_KEY"]


def predict(x_test, y_test, z_test, z_test_xpos):
    """Query the OpenAI API to predict lemmata of a list of sentences."""
    lemmata = []
    tokens = 0
    with open('../../nbs/openai_responses.txt', 'w', encoding='utf-8') as f:
        for sent in x_test:
            prompt = f"Lemmatisiere die Tokenliste: {sent}"
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=len(prompt)
            )
            answer = response["choices"][0]["text"]
            tokens += response['usage']['total_tokens']
            # response structure:
            # \n\n['lemma1', '...']
            try:
                lemmata.append(lemma.strip("'[]") for lemma in
                               answer.split('\n\n')[1].split("', "))
            except Exception as e:
                logger.error(e, answer)
            f.write(answer+'\n')
            time.sleep(3.)  # prevent rate limit errors
    print(f"{tokens} tokens used.")
    return lemmata


# run all benchmarks
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
