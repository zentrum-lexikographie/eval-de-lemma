THISFOLDER=$(pwd)
DATAFOLDER=datasets

# ArchiMob Release 2
# TODO check on lal
wget -c https://drive.switch.ch/index.php/s/vYZv9sNKetuPYTn/download -O ${DATAFOLDER}/Archimob_Release_2.zip
unzip -q ${DATAFOLDER}/Archimob_Release_2.zip -d ${DATAFOLDER}
mkdir ${DATAFOLDER}/archimob
mv ${DATAFOLDER}/Archimob_Release_2/Archimob_Release_2/* ${DATAFOLDER}/archimob
rm -r ${DATAFOLDER}/Archimob_Release_2
rm ${DATAFOLDER}/Archimob_Release_2.zip
