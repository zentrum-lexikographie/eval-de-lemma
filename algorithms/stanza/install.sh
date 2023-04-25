#!/usr/bin/env bash

SRCDIR=$(dirname "$0")

# install venv
python3 -m venv "${SRCDIR}/.venv"
source "${SRCDIR}/.venv/bin/activate"
pip install --upgrade pip
pip install -r "${SRCDIR}/requirements.txt"

# download models
python - <<EOF
import stanza
stanza.download('de')
EOF
