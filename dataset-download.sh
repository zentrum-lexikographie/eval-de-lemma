#!/bin/bash

THISFOLDER=$(pwd)
DATAFOLDER=datasets
mkdir -p ${DATAFOLDER}


# UD HDT, v2.10
wget -c https://github.com/UniversalDependencies/UD_German-HDT/archive/refs/tags/r2.10.zip -O ${DATAFOLDER}/ud-hdt.zip
unzip -q ${DATAFOLDER}/ud-hdt.zip -d ${DATAFOLDER}
mkdir ${DATAFOLDER}/ud-hdt
mv ${DATAFOLDER}/UD_German-HDT-r2.10/de_hdt-ud-test.conllu ${DATAFOLDER}/ud-hdt/de_hdt-ud-test.conllu 
rm -r ${DATAFOLDER}/UD_German-HDT-r2.10
rm ${DATAFOLDER}/ud-hdt.zip

# UD GSD, v2.10
wget -c https://github.com/UniversalDependencies/UD_German-GSD/archive/refs/tags/r2.10.zip -O ${DATAFOLDER}/ud-gsd.zip
unzip -q ${DATAFOLDER}/ud-gsd.zip -d ${DATAFOLDER}
mkdir ${DATAFOLDER}/ud-gsd
mv ${DATAFOLDER}/UD_German-GSD-r2.10/de_gsd-ud-test.conllu ${DATAFOLDER}/ud-gsd/de_gsd-ud-test.conllu
rm -r ${DATAFOLDER}/UD_German-GSD-r2.10
rm ${DATAFOLDER}/ud-gsd.zip

# UD PUD, v2.10
wget -c https://github.com/UniversalDependencies/UD_German-PUD/archive/refs/tags/r2.10.zip -O ${DATAFOLDER}/UD_German-PUD-r2.10.zip
unzip -q ${DATAFOLDER}/UD_German-PUD-r2.10.zip -d ${DATAFOLDER}
mkdir ${DATAFOLDER}/ud-pud
mv ${DATAFOLDER}/UD_German-PUD-r2.10/de_pud-ud-test.conllu ${DATAFOLDER}/ud-pud/de_pud-ud-test.conllu
rm -r ${DATAFOLDER}/UD_German-PUD-r2.10
rm -r ${DATAFOLDER}/UD_German-PUD-r2.10.zip

# GerManC
wget -c https://ota.bodleian.ox.ac.uk/repository/xmlui/bitstream/handle/20.500.12024/2544/2544.zip -O ${DATAFOLDER}/germanc.zip
unzip -q ${DATAFOLDER}/germanc.zip -d ${DATAFOLDER}/germanc
mv ${DATAFOLDER}/germanc/LING-COL/* ${DATAFOLDER}/germanc
rm ${DATAFOLDER}/germanc/*.{pdf,xlsx}
rm -r ${DATAFOLDER}/germanc/{LING-COL,LING-GATE,RAW,TEI}
rm ${DATAFOLDER}/germanc.zip

# ArchiMob Release 2
wget -c https://drive.switch.ch/index.php/s/vYZv9sNKetuPYTn/download -O ${DATAFOLDER}/Archimob_Release_2.zip
unzip -q ${DATAFOLDER}/Archimob_Release_2.zip -d ${DATAFOLDER}
mkdir ${DATAFOLDER}/archimob
mv ${DATAFOLDER}/Archimob_Release_2/*.xml ${DATAFOLDER}/archimob
rm -r ${DATAFOLDER}/Archimob_Release_2
rm ${DATAFOLDER}/Archimob_Release_2.zip

# NoSta-D
wget -c https://www.linguistik.hu-berlin.de/de/institut/professuren/korpuslinguistik/forschung/nosta-d/nosta-d-korpus-1.2 -O ${DATAFOLDER}/NoSta-D-Korpus-1.2.zip
mkdir ${DATAFOLDER}/nosta-d
unzip -q ${DATAFOLDER}/NoSta-D-Korpus-1.2.zip -d ${DATAFOLDER}/nosta-d
rm ${DATAFOLDER}/NoSta-D-Korpus-1.2.zip

# Empirist
wget -c https://github.com/fau-klue/empirist-lemmatization/archive/refs/heads/master.zip -O ${DATAFOLDER}/empirist2019.zip
unzip -q ${DATAFOLDER}/empirist2019.zip -d ${DATAFOLDER}
unzip -q ${DATAFOLDER}/empirist-lemmatization-master/data/empirist-lemmatization_training_data_2019-04-26.zip -d ${DATAFOLDER}
mv ${DATAFOLDER}/empirist-lemmatization_training_data_2019-04-26/train_web/lemmatized/ ${DATAFOLDER}/empirist2019-web-train
mv ${DATAFOLDER}/empirist-lemmatization_training_data_2019-04-26/train_cmc/lemmatized/ ${DATAFOLDER}/empirist2019-cmc-train
rm -r ${DATAFOLDER}/empirist-lemmatization_training_data_2019-04-26
rm -r ${DATAFOLDER}/empirist-lemmatization-master
rm ${DATAFOLDER}/empirist2019.zip