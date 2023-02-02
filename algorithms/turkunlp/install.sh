#!/usr/bin/env bash

SRCDIR=$(dirname "$0")

# clone repo
git clone https://github.com/TurkuNLP/Turku-neural-parser-pipeline.git
cd Turku-neural-parser-pipeline
git checkout orig-parser-pre-2021
git submodule update --init --recursive
cd "${SRCDIR}"

# install venv
python3.7 -m venv "${SRCDIR}/Turku-neural-parser-pipeline/.venv"
source "${SRCDIR}/Turku-neural-parser-pipeline/.venv/bin/activate"
pip install --upgrade pip
pip3 install wheel
pip install torch==0.4.1 -f https://download.pytorch.org/whl/torch_stable.html
pip install -r "${SRCDIR}/requirements.txt"
cd Turku-neural-parser-pipeline
python3 fetch_models.py de_gsd
cd "${SRCDIR}"