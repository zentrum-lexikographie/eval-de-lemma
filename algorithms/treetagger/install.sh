#!/usr/bin/env bash

SRCDIR=$(dirname "$0")

# install venv
python3.8 -m venv "${SRCDIR}/.venv"
source "${SRCDIR}/.venv/bin/activate"

# install treetagger
wget -c https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tree-tagger-linux-3.2.4.tar.gz
#tar –xvzf tree-tagger-linux-3.2.4.tar.gz –C
wget -c https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tagger-scripts.tar.gz
#tar –xvzf tagger-scripts.tar.gz -C
wget -c https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/install-tagger.sh
wget -c https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/german.par.gz
#tar -xvzf german.par.gz -C
#rm -r tree-tagger-linux-3.2.4.tar.gz
#rm -r tagger-scripts.tar.gz
#rm -r german.par.gz
sh install-tagger.sh

pip install --upgrade pip
pip install -r "${SRCDIR}/requirements.txt"