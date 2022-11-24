# -*- coding: utf-8 -*-
from .reader import (read_germanc, read_conllu, read_nostad,
                     read_txt, read_empirist, read_tgermacor)
import os
import glob


def load_data(DATASETSPATH):
    """
    Reads all tokens, gold lemmata and PoS-tags from a dataset.

    Parameters
    ----------
    DATASETSPATH : str
        Path to a dataset.

    Yields
    ------
    List[List[str], List[str], List[str]]
    x_test : List[str]
        List of tokens.
    y_test : List[str]
        List of lemmata.
    z_test : List[str]
        List of PoS-tags.
    dname : str
        Dataset name.

    """
    # default output
    x_test, y_test, z_test, dname = [], [], [], "n.a"

    # number of datasets
    n_datasets = 8

    for i in range(n_datasets):

        if i == 0:
            FILE = os.path.realpath(f"{DATASETSPATH}/ud-hdt/de_hdt-ud-test.conllu")
            x_test, y_test, z_test = read_conllu(FILE, lower_first=True)
            dname = "ud-hdt"

        elif i == 1:
            FILE = os.path.realpath(f"{DATASETSPATH}/ud-gsd/de_gsd-ud-test.conllu")
            x_test, y_test, z_test = read_conllu(FILE)
            dname = "ud-gsd"

        elif i == 2:
            FILE = os.path.realpath(f"{DATASETSPATH}/ud-pud/de_pud-ud-test.conllu")
            x_test, y_test, z_test = read_conllu(FILE, EOS='.')
            dname = "ud-pud"

        elif i == 3:
            x_test, y_test, z_test = [], [], []
            FILES = glob.glob(os.path.realpath(
                f"{DATASETSPATH}/germanc/*.txt"))
            for FILE in FILES:
                tmp = read_germanc(FILE, translit=True)
                x_test = x_test + tmp[0]
                y_test = y_test + tmp[1]
                z_test = z_test + tmp[2]
            dname = "germanc"

        elif i == 4:
            nosta_path = f"{DATASETSPATH}/nosta-d/"
            # list of subcorpora
            subcorpora = [s for s in os.listdir(nosta_path)
                          if os.path.isdir(os.path.join(nosta_path, s))]
            for corpus in subcorpora:
                # read each subcorpus seperately
                x_test, y_test, z_test = [], [], []
                for root, dirs, files in os.walk(os.path.join(nosta_path, corpus)):
                    for file in files:
                        if not file.endswith('_orig.tcf'):
                            continue  # include normalized files only
                        filepath = os.path.join(root, file).replace("\\", "/")
                        filepath = os.path.realpath(filepath)
                        tmp = read_nostad(filepath)
                        x_test = x_test + tmp[0]
                        y_test = y_test + tmp[1]
                        z_test = z_test + tmp[2]
                dname = f"nosta-d-{corpus}"
                print(dname)
                yield x_test, y_test, z_test, dname

        elif i == 5:
            x_test, y_test, z_test = [], [], []
            FILES = glob.glob(os.path.realpath(
                f"{DATASETSPATH}/empirist2019-cmc-train/*.txt"))
            for FILE in FILES:
                tmp = read_empirist(FILE)
                x_test = x_test + tmp[0]
                y_test = y_test + tmp[1]
                z_test = z_test + tmp[2]
            dname = "empirist-cmc"

        elif i == 6:
            x_test, y_test, z_test = [], [], []
            FILES = glob.glob(os.path.realpath(
                f"{DATASETSPATH}/empirist2019-web-train/*.txt"))
            for FILE in FILES:
                tmp = read_empirist(FILE)
                x_test = x_test + tmp[0]
                y_test = y_test + tmp[1]
                z_test = z_test + tmp[2]
            dname = "empirist-web"

        elif i == 7:
            FILE = os.path.realpath(f"{DATASETSPATH}/tgermacorp/TGermaCorp0.2_STTS.conll")
            # no upos tags, only xpos
            x_test, y_test, z_test = read_tgermacor(FILE)
            dname = "tgermacorp"

        if not dname.startswith('nosta-d'):
            # nosta-d data already yielded for each subcorpus
            print(dname)
            yield x_test, y_test, z_test, dname
