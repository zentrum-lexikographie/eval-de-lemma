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

# GerManC
wget -c https://ota.bodleian.ox.ac.uk/repository/xmlui/bitstream/handle/20.500.12024/2544/2544.zip -O ${DATAFOLDER}/germanc.zip
unzip -q ${DATAFOLDER}/germanc.zip -d ${DATAFOLDER}/germanc
mv ${DATAFOLDER}/germanc/LING-COL/* ${DATAFOLDER}/germanc
rm ${DATAFOLDER}/germanc/*.{pdf,xlsx}
rm -r ${DATAFOLDER}/germanc/{LING-COL,LING-GATE,RAW,TEI}
rm ${DATAFOLDER}/germanc.zip