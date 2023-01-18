#!/usr/bin/env bash

SRCDIR=$(dirname "$0")

# install venv
python3.7 -m venv "${SRCDIR}/.venv"
source "${SRCDIR}/.venv/bin/activate"

# install treetagger
mkdir tagger
cd tagger
wget -c https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tree-tagger-linux-3.2.4.tar.gz
wget -c https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tagger-scripts.tar.gz
wget -c https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/install-tagger.sh
wget -c https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/german.par.gz

sh install-tagger.sh
rm -r tree-tagger-linux-3.2.4.tar.gz
rm -r tagger-scripts.tar.gz
rm -r german.par.gz

cd ..

pip install --upgrade pip
pip install -r "${SRCDIR}/requirements.txt"