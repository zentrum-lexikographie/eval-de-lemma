#!/usr/bin/env bash

# clone repo
git clone https://github.com/TurkuNLP/Turku-neural-parser-pipeline.git
cd Turku-neural-parser-pipeline
git checkout orig-parser-pre-2021
git submodule update --init --recursive
cd ..

# install venv
python3.7 -m venv "Turku-neural-parser-pipeline/.venv"
source "Turku-neural-parser-pipeline/.venv/bin/activate"
pip install --upgrade pip
pip3 install wheel
pip install torch==0.4.1 -f https://download.pytorch.org/whl/torch_stable.html
pip install -r "requirements.txt"
cd Turku-neural-parser-pipeline
python3 fetch_models.py de_gsd
cd ..