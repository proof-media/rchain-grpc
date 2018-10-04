#!/usr/bin/env bash
S_KEY=`cat ./s_key.txt`

/opt/docker/bin/rnode \
    run -s -n \
    --host node1 \
    --data_dir ./data \
    --bonds-file ./bonds.txt \
    --wallets-file ./wallet.txt  \
    --validator-private-key $S_KEY
