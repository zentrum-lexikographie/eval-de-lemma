# eval-de-lemmatise
An evaluation study of lemmatizers on different German language corpora.

## Usage
In order to avoid python dependency conflicts, each lemmatizer is installed in a separate virtual environment.

```sh
for dir in algorithms/*; do
    bash "${dir}/install.sh"
done
```

Start the computations with the following command.

```sh
run.sh
```

The study has been conducted on TODO Ubuntu/linux version of LAL using Python7.

## Repository Structure
 * [algorithms](./algorithms) - seperate directory for each algorithm, each containing an install script (`install.sh`), overview of installed third party libraries (`requirements.txt`), and a run script (`run.py`)
	* [baseline](./algorithms/baseline) - baseline algorithm, lemma = surface form
	* [chatgpt](./algorithms/chatgpt): no need to run [run_api_queries.py](./algorithms/chatgpt/run_api_queries.py) yourself, you can also just execute [run.py](./algorithms/chatgpt/run.py) to evaluate the outputs of OpenAI queries from 20.-22.02.2023 (see [here](./nbs/chatgpt_outputs))
		* [run_api_queries.py](./algorithms/chatgpt/run_api_queries.py) - GPT-3 queries via the [OpenAI API](https://platform.openai.com/), to run this script, an OpenAI account and API key is needed, run `export OPEN_AI_KEY=INSERT_KEY_HERE` before executing the run script
	* [germalemma](./algorithms/germalemma)
	* [hanta](./algorithms/hanta)
	* [rnntagger](./algorithms/rnntagger)
	* [simplemma](./algorithms/simplemma)
	* [smorlemma](./algorithms/smorlemma)
	* [spacy2](./algorithms/spacy2)
	* [spacy3](./algorithms/spacy3)
	* [spacy3.3+](./algorithms/spacy3.3+)
	* [stanza](./algorithms/stanza)
	* [trankit](./algorithms/trankit)
	* [treetagger](./algorithms/treetagger)
	* [logs](./logs.log) - log file
 * [nbs](./nbs) - evaluation results and notebooks
    * [emissions](./nbs/emissions) - energy consumption of experiments
	* [lemmata](./nbs/lemmata) - lemmatizer outputs for qualitative evaluation
	* [evaluation.ipynb](./nbs/evaluation.ipynb) - quantitative evaluation of results
	* [evaluation-qualitative.ipynb](./nbs/evaluation-qualitative.ipynb) - qualitative evaluation of results
	* `results-*.json` - results of an algorithm, metrics calculated overall and by PoS tag
 * [src](./src) - source code scripts
   * [loader.py](./src/loader.py) - load the datasets
   * [metrics.py](./src/metrics.py) - evaluation metrics
   * [reader.py](./src/reader.py) - read functions for different types of datasets
   * [run.py](./src/run.py) - central run function to run an algorithm on a dataset and output the results to [nbs](./nbs)
   * [stts_to_upos.txt](./src/stts_to_upos.txt) - convert STTS to uPoS tags, based on [table](http://universaldependencies.org/docs/tagset-conversion/de-stts-uposf.html)
 * [dataset-download.sh](./dataset-download.sh) - download datasets
 * [README.md](./README.md)
 * [run.sh](./run.sh) - run all algorithms

## Datasets
TODO table with name, size, register

