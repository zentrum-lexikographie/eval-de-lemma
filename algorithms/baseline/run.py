import sys
import itertools
import json
import time
import tracemalloc

sys.path.append("../..")
from src.loader import load_data
from src.metrics import metrics_by_pos
#../../datasets
DATASETSPATH = "../../../lemma-data"

import warnings
warnings.filterwarnings("ignore")

# (A) Run all benchmarks
results = []
for x_test, y_test, z_test, dname in load_data(DATASETSPATH):
    try:
        # (A.1) encode labels and flatten sequences
        y_test = list(itertools.chain(*y_test))
        z_test = list(itertools.chain(*z_test))
        # (A.2) predict labels
        tracemalloc.start()
        t = time.time()
        # baseline lemmatization: lemma = token
        y_pred = x_test
        elapsed = time.time() - t
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        y_pred = list(itertools.chain(*y_pred))
        # (A.3) Compute metrics
        metrics = metrics_by_pos(y_test, y_pred, z_test)
        # Save results
        results.append({
            'dataset': dname, 'sample-size': len(y_test),
            'lemmatizer': 'baseline', 'metrics': metrics,
            'elapsed': elapsed, 'memory_current': current,
            'memory_peak': peak})
    except Exception as err:
        print(err)


# store results
with open("../../nbs/results-baseline.json", "w") as fp:
    json.dump(results, fp, indent=4)
