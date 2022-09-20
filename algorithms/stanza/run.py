import stanza
import sys
import itertools
import json
import pandas as pd
import time
import tracemalloc

sys.path.append("../..")
from src.loader import load_data
from src.metrics import metrics_by_pos

DATASETSPATH = "../../datasets"

import warnings
warnings.filterwarnings("ignore")


# (A) Load stanza model
model = stanza.Pipeline(
    lang='de', processors='tokenize,pos,lemma',
    tokenize_pretokenized=True)


# (B) Run all benchmarks
results = []

for x_test, y_test, z_test, dname in load_data(DATASETSPATH):
    try:
        # (B.1 encode labels and flatten sequences
        y_test = list(itertools.chain(*y_test))
        z_test = list(itertools.chain(*z_test))
        # (B.2) predict labels
        tracemalloc.start()
        t = time.time()
        docs = model(x_test)
        y_pred = [[t.lemma for t in sent.words] for sent in docs.sentences]
        elapsed = time.time() - t
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        y_pred = list(itertools.chain(*y_pred))
        x_test = list(itertools.chain(*x_test))
        # store and output different lemmatizations
        df = pd.DataFrame(columns=['token', 'lemma_gold', 'lemma_pred'])
        for i in range(len(y_test)):
            if y_test[i] != y_pred[i]:
                df.loc[i] = [x_test[i], y_test[i], y_pred[i]]
        df.to_csv(f"../../nbs/lemmata-stanza-{dname}.csv")
        # (B.3) Compute metrics
        metrics = metrics_by_pos(y_test, y_pred, z_test)
        # Save results
        results.append({
            'dataset': dname, 'sample-size': len(y_test),
            'lemmatizer': 'stanza', 'metrics': metrics,
            'elapsed': elapsed, 'memory_current': current,
            'memory_peak': peak})
    except Exception as err:
        print(err)


# store results
with open("../../nbs/results-stanza.json", "w") as fp:
    json.dump(results, fp, indent=4)
