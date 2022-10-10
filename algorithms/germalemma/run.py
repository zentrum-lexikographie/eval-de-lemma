import sys
import itertools
import json
import time
from germalemma import GermaLemma
import tracemalloc

sys.path.append("../..")
from src.loader import load_data
from src.metrics import metrics_by_pos

DATASETSPATH = "../../datasets"

import warnings
warnings.filterwarnings("ignore")


# instanciate lemmatizer, pass to function
lemmatizer = GermaLemma()


def lemmatize(token, pos):
    """predict a lemma given token and PoS tag"""
    try:
        return lemmatizer.find_lemma(token, pos)
    except Exception as e:
        # PoS tag not included
        return ""


# (A) Run all benchmarks
results = []

for x_test, y_test, z_test, dname in load_data(DATASETSPATH):
    try:
        # (A.1) encode labels and flatten sequences
        x_test = list(itertools.chain(*x_test))
        y_test = list(itertools.chain(*y_test))
        z_test = list(itertools.chain(*z_test))
        # (A.2) predict labels
        tracemalloc.start()
        t = time.time()
        y_pred = [lemmatize(x_test[i], z_test[i]) for i in range(len(x_test))]
        elapsed = time.time() - t
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        # store and output different lemmatizations of first 5000 tokens
        df = []
        j = 5000
        if len(y_test) < j:
            j = len(y_test)
        for i in range(j):
            if y_test[i] != y_pred[i]:
                df.append([x_test[i], y_test[i], y_pred[i]])
        with open(f"../../nbs/lemmata-germalemma-{dname}.json", "w") as fp:
            json.dump(df, fp, indent=4, ensure_ascii=False)
        # (A.3) Compute metrics
        metrics = metrics_by_pos(y_test, y_pred, z_test)
        # Save results
        results.append({
            'dataset': dname, 'sample-size': len(y_test),
            'lemmatizer': 'germalemma', 'metrics': metrics,
            'elapsed': elapsed, 'memory_current': current,
            'memory_peak': peak})
    except Exception as err:
        print(err)


# store results
with open("../../nbs/results-germalemma.json", "w") as fp:
    json.dump(results, fp, indent=4)
