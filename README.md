[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7821071.svg)](https://doi.org/10.5281/zenodo.7821071)

# eval-de-lemmatise
An evaluation study of lemmatizers on different German language corpora.
Branch [ba-lk](https://github.com/zentrum-lexikographie/eval-de-lemma/tree/ba-lk) contains the code for the Bachelor's thesis of Lydia Körber.

## Usage

1. Download the datasets.

```sh
bash dataset-download.sh
```

2. In order to avoid python dependency conflicts, each lemmatizer is installed in a separate virtual environment.

```sh
for dir in algorithms/*; do
    bash "${dir}/install.sh"
done
```

3. If you wish to track the CO2 emissions during the computation, execute [as described here](https://github.com/mlco2/codecarbon/issues/244):

```sh
sudo chmod -R a+r /sys/class/powercap/intel-rapl
```

Then start the computations with the following command.

```sh
bash run.sh
```

The study has been conducted on a Debian GNU/Linux 10 machine with 72 CPUs and 188 GB RAM using Python3.7.3.

(4.) To run the evaluation scripts in Jupyter Notebook, execute the following commands:

```sh
cd nbs
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
jupyter lab
```

## Data sets

| Data set (paper) | Format | Era | Genre | Language area | Guidelines | Annotation | Pre-processing |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| [Empirist 2019](https://aclanthology.org/2020.lrec-1.754/) | tab-separated | 21st c | a) dialogue (CMC): chat (social, professional), tweets, WhatsApp chats, blog comments, Wikipedia threads; b) web articles (Web) | DE | [link](https://github.com/fau-klue/empirist-lemmatization/blob/master/doc/lemmatisierungsrichtlinien.pdf), based on [TIGER](https://www.ims.uni-stuttgart.de/documents/ressourcen/korpora/tiger-corpus/annotation/tiger_scheme-morph.pdf) | manual | Normalized and original tokens used as input. |
| [GerManC-GS](https://aclanthology.org/W11-0415/) | XML | 1650 - 1800 (Early Modern German) | drama, humanities, legal texts, letters, narrative prose, newspapers, scientific texts, sermons | DE, AT, CH | [link](https://www.ids-mannheim.de/fileadmin/lexik/uwv/dateien/GerManC_Documentation.pdf) | manual | Normalized and original tokens used as input. Captions and stage directions ignored. |
| [NoSta-D](https://linguistics.rub.de/~dipper/pub/nosdac13.pdf) | TCF, XML | 14th - 21st c | historical (anselm), chat (unicum), spoken (bematac), learner (falko), literary prose (kafka), newspaper (tueba-dz) | DE | | semi-automatic (TreeTagger) | Normalized and original tokens used as input. |
| [RUB 2019](https://corpora.linguistik.uni-erlangen.de/data/konvens/proceedings/papers/KONVENS2019_paper_55.pdf), balanced | Conll-U | 20th - 21st c | Novelette, movie subtitles, sermon, TED talks, Wikipedia | DE | [TIGER](https://www.ims.uni-stuttgart.de/documents/ressourcen/korpora/tiger-corpus/annotation/tiger_scheme-morph.pdf) with some modifications | manual | UPOS tags are not available and need to be converted from XPOS tags (STTS). |
| [TGermaCorp](https://aclanthology.org/L16-1677) | Conll-U | 16th - 21st c | literature, Wikipedia | DE | | semi-automatic (TreeTagger) | |
| UD GSD, v2.10 (TIGER Korpus) | Conll-U | 21st c | daily newspaper (Frankfurter Rundschau) | DE | [link](https://www.ims.uni-stuttgart.de/documents/ressourcen/korpora/tiger-corpus/annotation/tiger_scheme-morph.pdf) | manual | |
| UD HDT, v2.10 (Hamburg Treebank) | Conll-U | 20th c | IT magazine (Heise) | DE | [link](https://edoc.sub.uni-hamburg.de/informatik/volltexte/2014/204/) | manual |  |
| UD PUD, v2.10 | Conll-U | 21st c | Wikipedia articles | DE | | manual |  |

## Repository Structure
 * [algorithms](./algorithms) - seperate directory for each algorithm, each containing an install script (`install.sh`), overview of installed third party libraries (`requirements.txt`), and a run script (`run.py`)
	* [baseline](./algorithms/baseline) - baseline algorithm, lemma = surface form
	* [gpt3](./algorithms/gpt3): no need to run [run_api_queries.py](./algorithms/gpt3/run_api_queries.py) yourself, you can also just execute [run.py](./algorithms/gpt3/run.py) to evaluate the outputs of OpenAI queries from 20.-22.02.2023 (outputs listed [here](./nbs/gpt3_outputs))
		* [run_api_queries.py](./algorithms/gpt3/run_api_queries.py) - GPT-3 queries via the [OpenAI API](https://platform.openai.com/), to run this script, an OpenAI account and API key is needed, run `export OPEN_AI_KEY=INSERT_KEY_HERE` before executing the run script
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
	* [gpt3_outputs](./nbs/gpt3_outputs) - outputs of OpenAI API queries 20.-22.02.2023 with [text-davinci-003](https://platform.openai.com/docs/models/gpt-3)
		* [formats.json](./nbs/gpt3_outputs/formats.json) - overview of different output formats of gpt-3 experiments
    * [emissions](./nbs/emissions) - energy consumption of experiments
	* [lemmata](./nbs/lemmata) - lemmatizer outputs for each corpus for qualitative evaluation
		* [all_lemmata.csv](./nbs/lemmata/all_lemmata.csv) - outputs of all lemmatizers on all corpora
	* [evaluation.ipynb](./nbs/evaluation.ipynb) - quantitative evaluation of results
	* [evaluation-gpt3.ipynb](./nbs/evaluation-gpt3.ipynb) - evaluation of outputs of GPT-3 queries
	* [evaluation-grauzonen.csv](./nbs/evaluation-grauzonen.csv) - extracts of [all_lemmata.csv](./nbs/lemmata/all_lemmata.csv) to analyze compund words, nominalized participles and adjective comparation
	* [evaluation-qualitative.ipynb](./nbs/evaluation-qualitative.ipynb) - preparing qualitative evaluation of results
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


