#!/usr/bin/env bash

SRCDIR=$(dirname "$0")

# install venv
python3.7 -m venv "${SRCDIR}/.venv"
source "${SRCDIR}/.venv/bin/activate"
pip install --upgrade pip
pip install -r "${SRCDIR}/requirements.txt"

# download models
python -m spacy download de_core_news_lg-2.3.0 --direct