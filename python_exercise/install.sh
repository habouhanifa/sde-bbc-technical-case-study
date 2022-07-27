#!/usr/bin/env bash
os=$(uname)

echo "OS System: $os"
DIR=.venv
PYTHON_VERSION=python3.7
LATEST_BACKUP=$(cat $DIR/_LATEST_INSTALL)
LATEST_ACTUAL=$(date -r requirements.txt +%Y-%m-%dT%H:%M:%S%z)

function print_header() {
    printf '#%.0s' {1..72}; echo
    echo -e "# $1"
    printf '#%.0s' {1..72}; echo
}


if [[ "${LATEST_BACKUP}" != "${LATEST_ACTUAL}" ]]; then


    print_header "Delete old sources"
    rm -Rf $DIR
    print_header "Install virtualenv"
    pip install virtualenv
    print_header "Install new virtual environment"
    python -m virtualenv -p $PYTHON_VERSION $DIR
    print_header "Activate the virtual environment"
    source ${DIR}/bin/activate
    print_header "Upgrade pip"
    python -m pip install --upgrade pip
    print_header "Install project requirements"
    python -m pip install -r requirements.txt 
    if [ $? = 0 ]; then
        echo "${LATEST_ACTUAL}" > $DIR/_LATEST_INSTALL
    fi
  
else
    print_header "Environment is up-to-date"
fi



