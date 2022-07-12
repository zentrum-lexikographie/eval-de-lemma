# -*- coding: utf-8 -*-
import conllu

def read_conllu(FILE: str, lower_first: bool=False):
    """Convert File in conllu format to a (x,y)-Dataset
    Parameters:
    -----------
    FILE : str
        The path to the data file
    lower_first : bool
        Transform the first lemma of a sentence to lower case (except from nouns)
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
                ztmp.append(tok['upos'])
        if (len(xtmp) >= 2) and (tok['xpos'] == '$.'):
            x.append(xtmp)
            y.append(ytmp)
            z.append(ztmp)
    return x, y, z


def read_germanc(FILE: str, translit: bool=True):
    # 1: original word, 2: transliteration
    if translit:
        colidx = 2
    else:
        colidx = 1

    # parse file
    x, y, z = [], [], []
    xtmp, ytmp, ztmp = [], [], []
    with open(FILE, "r", encoding="utf-8") as fp:
        for line in fp.readlines():
            dat = line.split('\t')
            if dat[0] != '\n':  # is not an empty line
                if len(dat[colidx]) > 0:  # word exists
                    xtmp.append(dat[colidx])  # word
                    ytmp.append(dat[4])  # lemma
                    ztmp.append(dat[3])  # tag
                    if dat[3] == "SENT":  # end of sentence
                        ztmp[-1] = '$.'
                        # minimum sequence length
                        if len(xtmp) >= 2:
                            x.append(xtmp)
                            y.append(ytmp)
                            z.append(ztmp)
                        xtmp, ytmp, ztmp = [], [], []

    return x, y, z  # token, lemma, PoS tag

print(read_germanc(r"C:\Users\Lydia\Documents\EVIDENCE\GermanC\LING-COL\DRAM_P1_OOD_1682_LiebesSig.txt")[1])