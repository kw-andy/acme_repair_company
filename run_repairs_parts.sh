#!/bin/bash

run_repairs_parts() {

if [ $# -lt 3 ]; then
    >&2 echo " 
    How to run 'run_repairs_parts.sh'?
    ./run_repairs_parts.sh url_to_fetch json_input_file json_output_file
    Ex: ./run_repairs_parts.sh 'https://www.vroomly.com/backend_challenge/labour_times' 'data.json' 'quotations.json'
    "
    exit 1
else
    export URL_TO_FETCH=$1
    export JSON_INPUT=$2
    export JSON_OUTPUT=$3
    python repairs_parts.py

fi

}

run_repairs_parts $1 $2 $3



