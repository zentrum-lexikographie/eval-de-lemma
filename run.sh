REPODIR=$(pwd)
for dir in algorithms/*; do
    echo ${dir}
    cd ${dir}
    source .venv/bin/activate
    python run.py
    deactivate
    cd ${REPODIR}
done
