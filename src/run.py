# -*- coding: utf-8 -*-
import csv
import gc
import itertools
import tracemalloc

from codecarbon import EmissionsTracker

from src.metrics import metrics_by_pos


def run_algorithm(predict, x_test, y_test, z_test, z_test_xpos, dname, aname) \
        -> dict:
    """Compute metrics on the outputs of a lemmatization tool on a corpus.

    Parameters
    ----------
    predict : funct
        Function to predict the lemmata of surface forms in x_test.
    x_test : List[List[str]]
        Nested list of tokens.
    y_test : List[List[str]]
        Nested list of gold standard lemmata.
    z_test : List[List[str]]
        Nested list of uPoS tags.
    z_test_xpos : List[List[str]]
        Nested list of xPoS tags (STTS).
    dname : str
        Name of the data set.
    aname : str
        Name of the lemmatization algorithm.

    Returns
    -------
    results : dict
        Includes dataset name, sample-size, lemmatizer name, metrics,
        elapsed_time, memory_current, memory_peak.
    """
    if not dname == 'chatgpt':
        # initialize tracker
        tracker = EmissionsTracker(
            output_file=f"../../nbs/emissions/emissions-{aname}.csv",
            on_csv_write="append")
        tracker.start()
        tracemalloc.start()
        # predict labels
        y_pred = predict(x_test, y_test, z_test, z_test_xpos)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        tracker.stop()
    else:  # read predictions from files
        y_pred = predict(x_test, dname)
        current, peak = 0, 0
    # flatten sequences
    y_test = list(itertools.chain(*y_test))
    z_test_xpos = list(itertools.chain(*z_test_xpos))
    if not aname == 'germalemma':  # germalemma flattened tokens, tags, lemmata
        # treetagger & rnntagger flattened lemmata
        if not (aname == 'treetagger' or aname == 'rnntagger'):
            y_pred = list(itertools.chain(*y_pred))
        x_test = list(itertools.chain(*x_test))
        z_test = list(itertools.chain(*z_test))
    # store and output lemmatizations of first 2000 tokens
    df = []
    j = 2000
    if len(y_test) < j:
        j = len(y_test)
    for i in range(j):
        # dataframe with token, upos tag, xpos tag, gold lemma, predicted lemma
        df.append([x_test[i], z_test[i], z_test_xpos[i], y_test[i], y_pred[i]])
    with open(f"../../nbs/lemmata/{dname}/{aname}-{dname}.csv", 'w',
              newline='', encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['token', 'tag', 'tag_STTS',
                            'lemma_gold', 'lemma_pred'])
        csvwriter.writerows(df)
    # compute metrics, considering content words only, certain PoS tags
    metrics = metrics_by_pos(y_test, y_pred, z_test, z_test_xpos)
    size = len(y_test)
    # delete variables, collect garbage
    del x_test, y_test, y_pred, z_test, z_test_xpos
    gc.collect()
    # save results
    return {
        'dataset': dname, 'sample-size': size,
        'lemmatizer': aname, 'metrics': metrics,
        'memory_current': current,
        'memory_peak': peak}
