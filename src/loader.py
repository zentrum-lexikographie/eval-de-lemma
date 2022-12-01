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
    n_datasets = 12

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
            # read each subcorpus seperately
            for corpus in subcorpora:
                # read the original and normalised versions seperately
                x_test, y_test, z_test = [], [], []
                x_test_norm, y_test_norm, z_test_norm = [], [], []
                for root, dirs, files in os.walk(os.path.join(nosta_path, corpus)):
                    for file in files:
                        filepath = os.path.join(root, file).replace("\\", "/")
                        filepath = os.path.realpath(filepath)
                        if file.endswith('_orig.tcf'):  # original files
                            tmp = read_nostad(filepath)
                            x_test = x_test + tmp[0]
                            y_test = y_test + tmp[1]
                            z_test = z_test + tmp[2]
                        else:  # normalised files
                            tmp = read_nostad(filepath, normalised=True)
                            x_test_norm = x_test_norm + tmp[0]
                            y_test_norm = y_test_norm + tmp[1]
                            z_test_norm = z_test_norm + tmp[2]
                dname = f"nosta-d-{corpus}-orig"
                print(dname)
                yield x_test, y_test, z_test, dname
                dname = f"nosta-d-{corpus}-norm"
                print(dname)
                yield x_test_norm, y_test_norm, z_test_norm, dname

        elif i == 5:
            x_test, x_test_norm, y_test, z_test = [], [], [], []
            FILES = glob.glob(os.path.realpath(
                f"{DATASETSPATH}/empirist2019-cmc-train/cmc_train_twitter*.txt"))
            for FILE in FILES:
                tmp = read_empirist(FILE)
                x_test = x_test + tmp[0]
                x_test_norm = x_test_norm + tmp[1]
                y_test = y_test + tmp[2]
                z_test = z_test + tmp[3]
            dname = "empirist-cmc-twitter"

        elif i == 6:
            x_test, x_test_norm, y_test, z_test = [], [], [], []
            FILES = glob.glob(os.path.realpath(
                f"{DATASETSPATH}/empirist2019-cmc-train/cmc_train_wiki*.txt"))
            for FILE in FILES:
                tmp = read_empirist(FILE)
                x_test = x_test + tmp[0]
                x_test_norm = x_test_norm + tmp[1]
                y_test = y_test + tmp[2]
                z_test = z_test + tmp[3]
            dname = "empirist-cmc-wiki"

        elif i == 7:
            FILE = glob.glob(os.path.realpath(
                f"{DATASETSPATH}/empirist2019-cmc-train/cmc_train_blog_comment.txt"))
            x_test, x_test_norm, y_test, z_test = read_empirist(FILE)
            dname = "empirist-cmc-blog"

        elif i == 8:
            FILE = glob.glob(os.path.realpath(
                f"{DATASETSPATH}/empirist2019-cmc-train/cmc_train_professional_chat.txt"))
            x_test, x_test_norm, y_test, z_test = read_empirist(FILE)
            dname = "empirist-cmc-chat-prof"

        elif i == 9:
            FILE = glob.glob(os.path.realpath(
                f"{DATASETSPATH}/empirist2019-cmc-train/cmc_train_social_chat.txt"))
            x_test, x_test_norm, y_test, z_test = read_empirist(FILE)
            dname = "empirist-cmc-chat-social"

        elif i == 10:
            FILE = glob.glob(os.path.realpath(
                f"{DATASETSPATH}/empirist2019-cmc-train/cmc_train_whats_app.txt"))
            x_test, x_test_norm, y_test, z_test = read_empirist(FILE)
            dname = "empirist-cmc-whatsapp"

        elif i == 11:
            x_test, x_test_norm, y_test, z_test = [], [], [], []
            FILES = glob.glob(os.path.realpath(
                f"{DATASETSPATH}/empirist2019-web-train/*.txt"))
            for FILE in FILES:
                tmp = read_empirist(FILE)
                x_test = x_test + tmp[0]
                x_test_norm = x_test_norm + tmp[1]
                y_test = y_test + tmp[2]
                z_test = z_test + tmp[3]
            dname = "empirist-web"

        elif i == 12:
            FILE = os.path.realpath(f"{DATASETSPATH}/tgermacorp/TGermaCorp0.2_STTS.conll")
            # no upos tags, only xpos
            x_test, y_test, z_test = read_tgermacor(FILE)
            dname = "tgermacorp"

        elif i == 13:
            FILE = os.path.realpath(f"{DATASETSPATH}/rub2019/novelette.conll")
            x_test, y_test, z_test = read_conllu(FILE)
            dname = "rub2019-novelette"

        elif i == 14:
            FILE = os.path.realpath(f"{DATASETSPATH}/rub2019/opensubtitles.conll")
            x_test, y_test, z_test = read_conllu(FILE)
            dname = "rub2019-subtitles"

        elif i == 15:
            FILE = os.path.realpath(f"{DATASETSPATH}/rub2019/sermononline.conll")
            x_test, y_test, z_test = read_conllu(FILE)
            dname = "rub2019-sermononline"

        elif i == 16:
            FILE = os.path.realpath(f"{DATASETSPATH}/rub2019/ted.conll")
            x_test, y_test, z_test = read_conllu(FILE)
            dname = "rub2019-ted"

        elif i == 17:
            FILE = os.path.realpath(f"{DATASETSPATH}/rub2019/wikipedia.conll")
            x_test, y_test, z_test = read_conllu(FILE)
            dname = "rub2019-wikipedia"

        if dname.startswith('empirist'):
            # yields normalised version of empirist corpus
            print(f'{dname}-norm')
            yield x_test_norm, y_test, z_test, f'{dname}-norm'
        if not dname.startswith('nosta-d'):
            # nosta-d data already yielded for each subcorpus
            print(dname)
            yield x_test, y_test, z_test, dname
