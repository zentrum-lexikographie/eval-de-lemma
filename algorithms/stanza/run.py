import stanza
import sys
import itertools
import json
import time

sys.path.append("../..")
from src.loader import load_data
from src.metrics import metrics_by_pos
#../../datasets
DATASETSPATH="../../../lemma-data"

import warnings
warnings.filterwarnings("ignore")


# (A) Load stanza model
model = stanza.Pipeline(
    lang='de', processors='tokenize,mwt,pos,lemma',
    tokenize_pretokenized=True)


# (B) Run all benchmarks
results = []
for x_test, y_test, z_test, dname in load_data(DATASETSPATH):
    try:
        # (B.1 encode labels and flatten sequences
        y_test = list(itertools.chain(*y_test))
        z_test = list(itertools.chain(*z_test))
        # (B.2) predict labels
        t = time.time()
        docs = model(x_test)
        y_pred = [[t.lemma for t in sent.words] for sent in docs.sentences]
        elapsed = time.time() - t
        y_pred = list(itertools.chain(*y_pred))
        # (B.3) Compute metrics
        metrics = metrics_by_pos(y_test, y_pred, z_test)
        # Save results
        results.append({
            'dataset': dname, 'sample-size': len(y_test),
            'lemmatizer': 'stanza', 'metrics': metrics,
            'elapsed': elapsed })
    except Exception as err:
        print(err)


# store results
with open("../../nbs/results-stanza.json", "w") as fp:
    json.dump(results, fp, indent=4)