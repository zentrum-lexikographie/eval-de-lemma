#!/usr/bin/env bash

SRCDIR=$(dirname "$0")

# clone repo
git clone https://github.com/TurkuNLP/Turku-neural-parser-pipeline.git
cd Turku-neural-parser-pipeline
git checkout orig-parser-pre-2021
git submodule update --init --recursive

# install venv
python3.7 -m venv "${SRCDIR}/.venv"
source "${SRCDIR}/.venv/bin/activate"
pip install --upgrade pip
pip3 install wheel
pip install torch==0.4.1 -f https://download.pytorch.org/whl/torch_stable.html
pip install -r "${SRCDIR}/requirements.txt"
python3 fetch_models.py de_gsd