#!/bin/bash

example_directories=$(find $(pwd)/ch*/s* -name '*.tf.json' -not -path '*/\.*' -not -path '*/_*' | xargs -I{} dirname {})

for directory in $example_directories; do
    echo "****** running terraform plan in ${directory} ******"
    cd ${directory} && terraform plan >/dev/null 2>&1
    if [ $? -eq 1 ]; then
        echo "plan failed"
    fi
done