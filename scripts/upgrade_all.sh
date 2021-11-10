#!/bin/bash

example_directories=$(find $(pwd)/ch*/s* -type d -not -path '*/\.*' -not -path '*/_*')

for directory in $example_directories; do
    echo "****** running terraform init in ${directory}... ******"
    cd ${directory} && terraform init -upgrade
    echo "****** running terraform validate in ${directory}... ******"
    cd ${directory} && terraform validate
    echo "****** running terraform fmt in ${directory}... ******"
    cd ${directory} && terraform fmt

    if test -f "${directory}/main.py"; then
        echo "****** running python main.py in ${directory}... ******"
        cd ${directory} && python main.py
    fi
done