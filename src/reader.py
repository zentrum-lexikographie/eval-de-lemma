# -*- coding: utf-8 -*-
import conllu
import logging
import os
from typing import List
from bs4 import BeautifulSoup

# logging settings
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="../logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s: %(message)s",
    datefmt="%y-%m-%d %H:%M:%S"
)

# initialize dict for stts to upos conversion
pos_dict = {}

with open(os.path.realpath('../../src/stts_to_upos.txt'), 'r',
          encoding='utf-8') as f:
    file = f.readlines()
    for line in file[1:]:
        pos, rest = line.split('=>')
        upos = rest.split('\t')[1]
        pos_dict[pos.strip()] = upos.strip()


def to_upos(xpos: List[List[str]]) -> List[List[str]]:
    """convert nested list of STTS tags to universal PoS tags"""
    d = [[pos_dict[p] if p in pos_dict.keys() else 'UNK' for p in sent]
         for sent in xpos]
    return d


def read_conllu(FILE: str, lower_first: bool = False, EOS: str = '$.'):
    """Convert File in conllu format to a (x,y)-Dataset
    Parameters:
    -----------
    FILE : str
        The path to the data file
    lower_first : bool
        Transform the first lemma of a sentence to lower case (except from nouns)
    EOS : str
        End-of-sentence universal STTS tag, usually '$.', but in case of PUD '.'
    Returns:
    --------
    examples: List[List[str], List[str], List[str]]
        All tokenized sequences with word tokens (x), lemmata (y) and PoS tags (z)
    """
    x, y, z = [], [], []
    with open(FILE, 'r', encoding='utf-8') as fp:
        corpus = conllu.parse(fp.read())
    for sents in corpus:
        xtmp, ytmp, ztmp = [], [], []
        for tok in sents:
            if len(tok['form']) > 0:
                xtmp.append(tok['form'])
                ylem = tok['lemma']
                if lower_first and sents.index(tok) == 0 \
                    and not tok['upos'] in {'NOUN', 'PROPN'}:
                    # lower first lemma, needed for HDT corpus
                    ylem = tok['lemma'].lower()
                ytmp.append(ylem)
                ztmp.append(tok['upos'])
        if (len(xtmp) >= 2) and (tok['xpos'] == EOS):
            x.append(xtmp)
            y.append(ytmp)
            z.append(ztmp)
    return x, y, z


def read_germanc(FILE: str, translit: bool = True):
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
    return x, y, to_upos(z)  # token, lemma, uPoS tag


def read_archimob(FILE: str):
    # parse file
    x, y, z = [], [], []
    xtmp, ytmp, ztmp = [], [], []
    with open(FILE, encoding='utf-8') as fp:
        f = fp.read()
    soup = BeautifulSoup(f, "lxml")
    sents = soup.find_all('u')
    for sent in sents:
        tokens = sent.find_all('w')
        for t in tokens:
            xtmp.append(t.text)
            ytmp.append(t['normalised'])
            ztmp.append(t['tag'])
        # minimum sequence length
        if len(xtmp) >= 2:
            x.append(xtmp)
            y.append(ytmp)
            z.append(ztmp)
        xtmp, ytmp, ztmp = [], [], []
    return x, y, to_upos(z)  # token, lemma, uPoS tag


def read_nostad(FILE: str):
    # parse file
    x, y, z = [], [], []
    xtmp, ytmp, ztmp = [], [], []
    with open(FILE, encoding='utf-8') as fp:
        f = fp.read()
    soup = BeautifulSoup(f, "lxml")
    tokens = {t['id']: t.text for t in soup.find_all('ns3:token')}
    lemmata = {t['tokenids']: t.text for t in soup.find_all('ns3:lemma')}
    pos = {t['tokenids']: t.text for t in soup.find_all('ns3:tag')}
    for ID in tokens.keys():
        try:  # some tokens are not lemmatized
            ytmp.append(lemmata[ID])
            xtmp.append(tokens[ID])
            ztmp.append(pos[ID])
        except Exception as e:
            logger.error(e)
        if ztmp and ztmp[-1] == '$.' and len(xtmp) >= 2:  # EOS
            x.append(xtmp)
            y.append(ytmp)
            z.append(ztmp)
            xtmp, ytmp, ztmp = [], [], []
    return x, y, to_upos(z)  # token, lemma, uPoS tag

def read_txt(FILE: str):
    # annotation oriented at PUD corpus
    x, y, z = [], [], []
    xtmp, ytmp, ztmp = [], [], []
    with open(FILE, encoding='utf-8') as fp:
        sents = fp.read().split('\n\n')
    for sent in sents:
        tokens, lemmata, tags = sent.split('\n')
        tokens = tokens.split(' ')
        lemmata = lemmata.split(' ')
        tags = tags.split(' ')
        x.append(tokens)
        y.append(lemmata)
        z.append(tags)
    return x, y, z  # token, lemma, uPoS tag
