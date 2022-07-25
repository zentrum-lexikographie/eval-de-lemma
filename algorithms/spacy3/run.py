import sys
import itertools
import json
import time
import spacy

sys.path.append("../..")
from src.loader import load_data
from src.metrics import metrics_by_pos
#../../datasets
DATASETSPATH="../../../lemma-data"

import warnings
warnings.filterwarnings("ignore")

# (A) Instanciate SpaCy model
nlp = spacy.load('de_dep_news_trf')

# (B) Run all benchmarks
results = []
for x_test, y_test, z_test, dname in load_data(DATASETSPATH):
    try:
        # (B.1) encode labels and flatten sequences
        y_test = list(itertools.chain(*y_test))
        z_test = list(itertools.chain(*z_test))
        # (B.2) predict labels
        t = time.time()
        y_pred = [w.lemma_ for w in [nlp(' '.join(s)) for s in x_test]]
        elapsed = time.time() - t
        y_pred = list(itertools.chain(*y_pred))
        # (B.3) Compute metrics
        metrics = metrics_by_pos(y_test, y_pred, z_test)
        # Save results
        results.append({
            'dataset': dname, 'sample-size': len(y_test),
            'lemmatizer': 'spacy3', 'metrics': metrics,
            'elapsed': elapsed})
    except Exception as err:
        print(err)


# store results
with open("../../nbs/results-spacy3.json", "w") as fp:
    json.dump(results, fp, indent=4)
