#!/usr/bin/env bash

python setup.py develop
pip install -r requirements_dev.txt

./wait-for-it.sh $RCHAIN_GRPC_HOST:40401 -t 3600

if [ "$1" = "watch" ]; then
    ptw
else
    python setup.py test
fi
