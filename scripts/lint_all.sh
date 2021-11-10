#!/bin/bash

example_directories=$(find $(pwd)/ch*/s* -type d -not -path '*/\.*' -not -path '*/_*')

for directory in $example_directories; do
    echo "****** running autoflake in ${directory}... ******"
    cd ${directory} && autoflake --in-place --remove-unused-variables --remove-all-unused-imports .
done