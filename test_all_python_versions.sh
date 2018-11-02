#!/bin/bash
set -e

for version in $(seq 36 37);
do
    echo
    echo "Running tests on python v$version"
    docker-compose run --rm tests-$version
    if [ "$?" != "0" ]; then
        echo "Failed for $version"
        exit 0
    fi
done

echo completed
