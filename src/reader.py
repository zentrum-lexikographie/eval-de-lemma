# -*- coding: utf-8 -*-
import conllu

def read_conllu(FILE: str, lower_first=False):
    """Convert File from Empirist Shared Task to a (x,y)-Dateset
    Parameters:
    -----------
    FILE : str
        The path to the data file
    lower_first : bool
        Transform the first lemma of a sentence to lower case
    Returns:
    --------
    examples: List[List[str], List[str], List[str]]
        All tokenized sequences with word tokens (x), lemmata (y) and PoS tags (z)
    """
    x, y, z = [], [], []
    with open(FILE, 'r') as fp:
        corpus = conllu.parse(fp.read())
    for sents in corpus:
        xtmp, ytmp, ztmp = [], [], []
        for tok in sents:
            if len(tok['form']) > 0:
                xtmp.append(tok['form'])
                ylem = tok['lemma']
                if lower_first and sents.index(tok) == 0 \
                    and not tok['upos'] in {'NOUN', 'PROPN'}:
                  ylem = tok['lemma'].lower()  # lower first lemma, needed for HDT corpus
                ytmp.append(ylem)
                ztmp.append(tok['xpos'])
        if (len(xtmp) >= 2) and (tok['xpos'] == '$.'):
            x.append(xtmp)
            y.append(ytmp)
            z.append(ztmp)
    return x, y, z

