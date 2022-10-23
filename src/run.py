# -*- coding: utf-8 -*-
import itertools
import json
import time
import tracemalloc

from src.metrics import metrics_by_pos


def run_algorithm(predict, x_test, y_test, z_test, dname, aname):
    """
    Computes metrics on the outputs of a lemmatization tool on a corpus.

    Parameters
    ----------
    predict : funct
        a function to predict the lemma of x_test
    x_test : TYPE
        DESCRIPTION.
    z_test : TYPE
        DESCRIPTION.
    dname : str
        DESCRIPTION.
    aname : str
        name of the algorithm.

    Returns
    -------
    None.

    """
    # (A.1) encode labels and flatten sequences
    y_test = list(itertools.chain(*y_test))
    z_test = list(itertools.chain(*z_test))
    # (A.2) predict labels
    tracemalloc.start()
    t = time.time()
    y_pred = predict(x_test, y_test, z_test)
    elapsed = time.time() - t
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    if not aname == 'germalemma':
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
    with open(f"../../nbs/lemmata-{aname}-{dname}.json", "w") as fp:
        json.dump(df, fp, indent=4, ensure_ascii=False)
    # (A.3) Compute metrics
    metrics = metrics_by_pos(y_test, y_pred, z_test)
    # Save results
    return {
        'dataset': dname, 'sample-size': len(y_test),
        'lemmatizer': 'baseline', 'metrics': metrics,
        'elapsed': elapsed, 'memory_current': current,
        'memory_peak': peak}
