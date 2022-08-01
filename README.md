# eval-de-lemmatise

## Usage
Um Versionskonflikte zu vermeiden wird jeder Lemmatisierer in einer seperaten virtuellen Python-Umgebung installiert. 
(In order to avoid python dependency conflicts, each lemmatizer gets its own virtual environment.)

```sh
# rm -r algorithms/*/.venv

for dir in algorithms/*; do
    bash "${dir}/install.sh"
done
```

Die Berechnungen werden mit folgenden CLI-Befehl ausgeführt. (Start the computations with the following command.)

```sh
REPODIR=$(pwd)
for dir in algorithms/*; do
    echo ${dir}
    cd ${dir}
    source .venv/bin/activate
    python run.py
    deactivate
    cd ${REPODIR}
done
```