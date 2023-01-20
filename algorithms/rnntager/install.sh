#!/usr/bin/env bash

SRCDIR=$(dirname "$0")

# install venv
python3.7 -m venv "${SRCDIR}/.venv"
source "${SRCDIR}/.venv/bin/activate"
pip install --upgrade pip
pip install -r "${SRCDIR}/requirements.txt"

# install tagger
mkdir tagger
cd tagger
wget -c https://www.cis.uni-muenchen.de/~schmid/tools/RNNTagger/data/RNNTagger-1.3.0.zip
unzip RNNTagger-1.3.0.zip
rm -r RNNTagger-1.3.0.zip