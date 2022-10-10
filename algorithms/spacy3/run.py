import sys
import itertools
import json
import time
import spacy
import tracemalloc

sys.path.append("../..")
from src.loader import load_data
from src.metrics import metrics_by_pos

DATASETSPATH = "../../datasets"

import warnings
warnings.filterwarnings("ignore")

# (A) Instanciate SpaCy model
model = spacy.load('de_dep_news_trf')
model.disable_pipes(["parser"])

# (B) Run all benchmarks
results = []

for x_test, y_test, z_test, dname in load_data(DATASETSPATH):
    try:
        # (B.1) encode labels and flatten sequences
        y_test = list(itertools.chain(*y_test))
        z_test = list(itertools.chain(*z_test))
        # (B.2) predict labels
        tracemalloc.start()
        t = time.time()
        lemmatizer = model.pipeline[4][1]
        docs = [lemmatizer(spacy.tokens.doc.Doc(model.vocab, words=sequence))
                for sequence in x_test]
        y_pred = [[w.lemma_ for w in doc] for doc in docs]
        elapsed = time.time() - t
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        y_pred = list(itertools.chain(*y_pred))
        x_test = list(itertools.chain(*x_test))
        # store and output different lemmatizations of first 5000 tokens
        df = []
        j = 5000
        if len(y_test) < j:
            j = len(y_test)
        for i in range(j):
            if y_test[i] != y_pred[i]:
                df.append([x_test[i], y_test[i], y_pred[i]])
        with open(f"../../nbs/lemmata-spacy3-{dname}.json", "w") as fp:
            json.dump(df, fp, indent=4, ensure_ascii=False)
        # (B.3) Compute metrics
        metrics = metrics_by_pos(y_test, y_pred, z_test)
        # Save results
        results.append({
            'dataset': dname, 'sample-size': len(y_test),
            'lemmatizer': 'spacy3', 'metrics': metrics,
            'elapsed': elapsed, 'memory_current': current,
            'memory_peak': peak})
    except Exception as err:
        print(err)


# store results
with open("../../nbs/results-spacy3.json", "w") as fp:
    json.dump(results, fp, indent=4)
