#!/usr/bin/env bash

SRCDIR=$(dirname "$0")

# download transducer
wget -c https://pub.cl.uzh.ch/users/sennrich/zmorge/transducers/zmorge-20150315-smor_newlemma.ca.zip
unzip -q zmorge-20150315-smor_newlemma.ca.zip
rm zmorge-20150315-smor_newlemma.ca.zip

# download lexicon
wget -c https://pub.cl.uzh.ch/users/sennrich/zmorge/lexica/zmorge-20150315.xml.zip
unzip -q zmorge-20150315.xml.zip
rm zmorge-20150315.xml.zip

# install venv
python2.6 -m venv "${SRCDIR}/.venv"
source "${SRCDIR}/.venv/bin/activate"
pip install --upgrade pip
pip install -r "${SRCDIR}/requirements.txt"

# install smorlemma
sudo apt-get install build-essential xsltproc sfst

git clone git@github.com:rsennrich/SMORLemma.git
cd SMORLemma
git checkout lemmatiser
cp ../zmorge-20150315.xml lexicon/wiki-lexicon.xml
make

