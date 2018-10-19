#!/usr/bin/env bash

python setup.py develop
pip install -r requirements_dev.txt

#########################
# HACK to skip issue:
# https://github.com/protocolbuffers/protobuf/issues/5272
cd /usr/local/lib/python3.7/site-packages/protobuf-*-py3.7.egg/google/protobuf/internal/
rm python_message.py*
wget https://raw.githubusercontent.com/pdonorio/protobuf/rchain-workaround/python/google/protobuf/internal/python_message.py
cd -
#########################

./wait-for-it.sh $RCHAIN_GRPC_HOST:40401 -t 3600

if [ "$1" = "watch" ]; then
    ptw
else
    python setup.py test
fi
