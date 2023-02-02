#!/usr/bin/env bash

# clone repo
git clone https://github.com/TurkuNLP/Turku-neural-parser-pipeline.git
cd Turku-neural-parser-pipeline
git checkout orig-parser-pre-2021
git submodule update --init --recursive

# install venv
python3.7 -m venv ".venv"
source ".venv/bin/activate"
pip install --upgrade pip
pip3 install wheel
pip install torch==0.4.1 -f https://download.pytorch.org/whl/torch_stable.html
pip install -r "../requirements.txt"
python3 fetch_models.py de_gsd
cd ..