# -*- coding: utf-8 -*-
import logging
import os
from typing import List

from bs4 import BeautifulSoup
import conllu

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
pos_dict['PROAV'] = 'ADV'  # tag missing in list

# fill pos_dict, structure {xPoS: uPoS}
with open(os.path.realpath('../../src/stts_to_upos.txt'), 'r',
          encoding='utf-8') as f:
    file = f.readlines()
    for line in file[1:]:
        pos, rest = line.split('=>')
        upos = rest.split('\t')[1]
        pos_dict[pos.strip()] = upos.strip()


def to_upos(xpos: List[List[str]]) -> List[List[str]]:
    """Convert a nested list of STTS tags to universal PoS tags."""
    return [[pos_dict[p] if p in pos_dict.keys() else 'UNK' for p in sent]
            for sent in xpos]


def read_conllu(FILE: str, lower_first: bool = False, EOS: str = '$.',
                upos: bool = True) \
        -> List[List[str], List[str], List[str], List[str]]:
    """Convert a file in conllu format to a (x,y,z,z_xpos)-dataset.

    Parameters:
    -----------
    FILE : str
        The path to the data file.
    lower_first : bool
        Transform the first lemma of a sentence to lower case
        (except from nouns).
    EOS : str
        End-of-sentence universal STTS tag, usually '$.',
        but in case of PUD '.'.
    upos : bool
        True if uPoS tags are available.

    Returns:
    --------
        All tokenized sequences as nested lists of word tokens (x),
        lemmata (y), uPoS tags (z) and xPoS tags (z_xpos).
    """
    x, y, z, z_xpos = [], [], [], []
    with open(FILE, 'r', encoding='utf-8') as fp:
        corpus = conllu.parse(fp.read())
    for sents in corpus:
        xtmp, ytmp, ztmp, z_xpostmp = [], [], [], []
        for tok in sents:
            if len(tok['form']) > 0:
                xtmp.append(tok['form'])
                ylem = tok['lemma']
                if tok['xpos'] in pos_dict.keys():
                    # prevent keyerror
                    if lower_first and sents.index(tok) == 0 \
                            and not pos_dict[tok['xpos']] in {'NOUN', 'PROPN'}:
                        # lower first lemma, needed for HDT corpus
                        ylem = tok['lemma'].lower()
                ytmp.append(ylem)
                if upos:
                    ztmp.append(tok['upos'])
                else:
                    ztmp.append(tok['xpos'])
                z_xpostmp.append(tok['xpos'])
        if (len(xtmp) >= 2) and (tok['xpos'] == EOS):
            x.append(xtmp)
            y.append(ytmp)
            z.append(ztmp)
            z_xpos.append(z_xpostmp)
    if not upos:  # conversion of STTS to uPoS tags
        z = to_upos(z)
    return x, y, z, z_xpos


def read_germanc(FILE: str, translit: bool = True) \
        -> List[List[str], List[str], List[str], List[str]]:
    """Convert a file from GermanC corpus to a (x,y,z,z_xpos)-dataset.

    Parameters:
    -----------
    FILE : str
        The path to the data file.
    translit : bool
        If set to True, the transliterated form of the token is used instead
        of the original, e.g. "kömmet" instead of "koͤmmet".

    Returns:
    --------
        All tokenized sequences as nested lists of word tokens (x),
        lemmata (y), uPoS tags and xPoS tags (z).
    """
    #  column index: 1 (original word), 2 (transliteration)
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
    return x, y, to_upos(z), z  # token, lemma, uPoS tag, xPoS tag


def read_nostad(FILE: str, normalised: bool = False) \
        -> List[List[str], List[str], List[str], List[str]]:
    """Convert a file from NoSta-D corpus to a (x,y,z,z_xpos)-dataset.

    Parameters:
    -----------
    FILE : str
        The path to the data file.
    normalised : bool
        If set to True, the normalised form of the file is used instead
        of the original (no orthographic variation, ellipses corrected).

    Returns:
    --------
        All tokenized sequences as nested lists of word tokens (x),
        lemmata (y), uPoS tags and xPoS tags (z).
    """
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
        try:  # some tokens are not lemmatized because they only appear in
            # one version, original or normalized, ID still exists in both
            ytmp.append(lemmata[ID])
            xtmp.append(tokens[ID])
            ztmp.append(pos[ID])
        except Exception:
            pass
        if ztmp and ztmp[-1] == '$.' and len(xtmp) >= 2:  # EOS
            x.append(xtmp)
            y.append(ytmp)
            z.append(ztmp)
            xtmp, ytmp, ztmp = [], [], []
    return x, y, to_upos(z), z  # token, lemma, uPoS tag, xPoS tag


def read_empirist(FILE: str) \
        -> List[List[str], List[str], List[str], List[str]]:
    """Convert a file from Empirist corpus to a (x,y,z,z_xpos)-dataset,
    including original and normalised tokens.

    Parameters:
    -----------
    FILE : str
        The path to the data file.

    Returns:
    --------
        All tokenized sequences as nested lists of word tokens (x), normalized
        word tokens (x_norm), lemmata (y), uPoS tags and xPoS tags (z).
    """
    # parse file
    x, x_norm, y, z = [], [], [], []
    xtmp, xtmp_norm, ytmp, ztmp = [], [], [], []
    with open(FILE, encoding='utf-8') as fp:
        f = fp.read()
    sents = f.split('\n\n')  # postings
    for s in sents:
        for line in s.split('\n')[1:]:  # first line contains ID
            if line:
                # use normalised or original token, normalised lemma
                token, tag, token_norm, lemma, lemma_norm = \
                    line.strip().split('\t')
                xtmp.append(token)  # original token
                xtmp_norm.append(token_norm)  # normalised token
                ytmp.append(lemma_norm)  # normalised lemma
                ztmp.append(tag)
        x.append(xtmp)
        x_norm.append(xtmp_norm)
        y.append(ytmp)
        z.append(ztmp)
        xtmp, xtmp_norm, ytmp, ztmp = [], [], [], []
    # token, normalized token, lemma, uPoS tag, xPoS tag
    return x, x_norm, y, to_upos(z), z


def read_tgermacor(FILE: str, EOS: str = '$.') \
        -> List[List[str], List[str], List[str], List[str]]:
    """Convert a file from TGermaCorpus to a (x,y,z,z_xpos)-dataset.

    Parameters:
    -----------
    FILE : str
        The path to the data file.
    EOS : str
        End-of-sentence universal STTS tag, usually '$.',
        but in some cases '.'

    Returns:
    --------
        All tokenized sequences as nested lists of word tokens (x),
        lemmata (y), uPoS tags and xPoS tags (z).
    """
    x, y, z = [], [], []
    with open(FILE, 'r', encoding='utf-8') as fp:
        corpus = fp.read()
    sents = corpus.split('\n\n')
    for sent in sents:  # iterate sentences
        xtmp, ytmp, ztmp = [], [], []
        for tok in sent.split('\n'):  # iterate tokens
            if not tok:  # empty string in line end
                continue
            ID, token, lemma, _, xpos = tok.split()[:5]
            xtmp.append(token)
            ytmp.append(lemma)
            ztmp.append(xpos)
        if (len(xtmp) >= 2) and (xpos == EOS):
            # end of sentence reached
            x.append(xtmp)
            y.append(ytmp)
            z.append(ztmp)
    return x, y, to_upos(z), z
