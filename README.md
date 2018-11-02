
## rchain-grpc

| package | tests | updates |
| --- | --- | --- |
| [![image](https://img.shields.io/pypi/v/rchain-grpc.svg)](https://pypi.python.org/pypi/rchain-grpc) | [![image](https://travis-ci.com/proof-media/rchain-grpc.svg?branch=master)](https://travis-ci.com/proof-media/rchain-grpc) | [![Updates](https://pyup.io/repos/github/proof-media/rchain-grpc/shield.svg)](https://pyup.io/repos/github/proof-media/rchain-grpc/)

Python3 client for RChain nodes gRPC protocol

*   Free software: MIT license
*   Documentation: [https://proof-media.github.io/rchain-grpc](https://proof-media.github.io/rchain-grpc)


## About this package

This project aims at giving to Python users an easy way to interact with the RChain blockchain.
Since RChain nodes run [gRPC](https://grpc.io/docs/) servers (by default on port `40401`), this library is built as a Python client with an up-to-date sets of (small) API that sends and receives data through the protocol.


## About the RChain blockchain platform

RChain is a new and unique approach to build the blockchain platform for the next generation. You can deploy written in `rholang` smart contracts on RChain nodes.

Here are the main references for the project:

- The main [web site](https://www.rchain.coop/)
- A gentle [introduction](https://blog.coinfund.io/an-introduction-to-rchain-d5fe303e9fe1) to the RChain world
- Run your own node following [instructions](https://rchain.atlassian.net/wiki/spaces/CORE/pages/428376065/User+guide+for+running+RNode) or with [docker](https://hub.docker.com/r/rchain/rnode/)
- Learn how to [write rholang](https://www.rchain.coop/learn-rholang) and try it [in the cloud](https://rchain.cloud/)
- Details about [the latest RNode release](https://www.rchain.coop/blog/release-of-rnode-v0-7-1/)

You can reach out to the community and developers on [discord](https://discordapp.com/channels/375365542359465989/375365542854262785) and decide to [become a member of the cooperative](https://member.rchain.coop/)


## Current available features

*   Connecting to RChain `rnode` through gRPC protocol
*   Listing blocks and dumping tuple-space from one.
*   Deploying `rholang` contracts and propose new blocks
*   Listening for streams of data when proposing blocks


## Python supported versions

This code is tested on latest `Python3.6` and `Python3.7` releases only.


## Compatibility with Rchain versions

Rchain is beeing developed as we speak, be careful on which version of this package you install:

* Releases <= `0.0.10` are compatible with `RNode 0.6.x`
* `0.7.x` is compatible with `RNode 0.7.x`
* `0.8.x` will be compatible with `RNode 0.8.x`
* etc.


## Installation

Recommended way to install the package is to use the official python package manager, e.g. from command line:

```bash
pip install rchain-grpc
```

You can also download the package in the [Pypi web site](https://pypi.org/project/rchain-grpc/#files).

NOTE: you can test the library by just running a docker container:
```bash
docker run \
    --rm --interactive --tty --entrypoint /bin/bash \
    python:3.7 \
    -c "pip install rchain-grpc ipython && ipython"

In [1]: import rchain_grpc

In [2]: rchain_grpc.__version__
Out[2]: '0.7.0'
```


## Code examples

This project is a wrapper to simplify the use of gRPC interaction with RChain networks. Here we describe now the main examples you can use it with.


### create a connection to a running node

To connect to a running RChain Casper network you need to create the connection object:

```python
from rchain_grpc import casper

rnode_host = '...'  # valid IP of running node
rnode_port = 40401  # default
connection = casper.create_connection(host=rnode_host, port=rnode_port)
```


### deploy a rholang contract

Contracts written in `rholang` use the `.rho` file extension.
You can read one and deploy it to the rnode using the connection object:

```python
rholang_file = 'hello_world.rho'
with open(rholang_file) as fh:
    rholang_code = fh.read()

# deploy the code and create the new block for the current rchain blockchain

casper.deploy(connection, rholang_code)
>>> {'success': True, 'message': 'Success!'}
casper.propose(connection)
>>> {'success': True, 'message': 'Success! Block 33a9183ff0... created and added.'}

# watch the RNode logs for any stdout
# or to verify the same block hash

```

Note that the `rholang_code` is just a string with `rholang` valid instructions, you can write your own inside Python too.


### get blocks

Get the latest block hash:
```python
casper.get_blocks(connection, depth=1)

>>> [{'blockHash': '33a9183ff02c17f9d55d0a087be453163bc39fd07a3d19f3fac10a67286a6135',
  'blockSize': '1340',
  'blockNumber': 1,
  'deployCount': 1,
  'tupleSpaceHash': '477f7f0c469de6d500d8a1f74852a4ecf49df9a7fa463207d62258161bf39fb7',
  'timestamp': 1540906627156,
  'faultTolerance': -1.0,
  'mainParentHash': 'd85ee52cec7c09e301cef8ad2d3b3e807defc54f92d391f75c96a366c878d54a',
  'parentsHashList': ['d85ee52cec7c09e301cef8ad2d3b3e807defc54f92d391f75c96a366c878d54a'],
  'sender': 'eabe5a1a0750d2a8745709bb0bdb24f63c6a8ac3a887b9bed40b34b0598ddf08'}]

# NOTE: protobuf outputs are always converted into Python dictionaries
# automatically by our library
```

Once you know a block hash you can get detailed informations and a dump of tuplespace directly:

```python
output = casper.get_blocks(connection)
block_hash = output.pop().get('blockHash')
block = casper.get_block(connection, block_hash=block_hash)

print(block.get('tupleSpaceDump'))

# [...]
# lots of code output
```


### context manager

The connection provided by the library can be used inside a `with` statement:

```python
# all previous operations in one context

with casper.create_connection(host=rnode_host) as connection:

    # deploy / propose
    casper.deploy(connection, rholang_code)
    print(casper.propose(connection))

    # handle output
    output = casper.get_blocks(connection, depth=1)
    block_hash = output.pop().get('blockHash')
    block = casper.get_block(connection, block_hash=block_hash)
    print(f"Current block number is {block.get('blockNumber')}\nwith hash {block_hash}")

# NOTE: connection here is closed
```


### interact with channels

In a more advanced use case, we could also specify a `channel` to listen to:

```python
output_placeholder = "your_channel_name"
# A rholang contract that sends 'bar' string to our channel
rholang_code = f"""
{output_placeholder}!("bar")
"""

with casper.create_connection(host=rnode_host) as connection:
    block = casper.run_and_get_value_from(
        connection, rholang_code,
        output_placeholder=output_placeholder
    )

    results = block.get('blockResults').pop()
    for message in results.get('postBlockData'):
        print("Received: ", message.pop())

    # here we get 'bar' back
```


### name registry

to do


## Other media

*   [Recorded walk-through](youtu.be/H_pmVff7c3Q) and [slides](https://nbviewer.jupyter.org/format/slides/github/proof-media/rchain-notebook/blob/master/notebooks/walk-through.ipynb#/) for the rchain discord community
*   [Notebook examples](https://github.com/proof-media/rchain-notebook) running on this [container image](https://hub.docker.com/r/proofmedia/rchain-notebook/) (see also [Dockerfile](https://github.com/proof-media/rchain-notebook/tree/master/builds/notebooker))
