
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


## Code examples

This project is a wrapper to simplify the use of gRPC interaction with RChain networks. The use cases are very simple!

### bla

bla



## Other media

*   [Recorded walk-through](youtu.be/H_pmVff7c3Q) and [slides](https://nbviewer.jupyter.org/format/slides/github/proof-media/rchain-notebook/blob/master/notebooks/walk-through.ipynb#/) for the rchain discord community
*   [Notebook examples](https://github.com/proof-media/rchain-notebook) running on this [container image](https://hub.docker.com/r/proofmedia/rchain-notebook/) (see also [Dockerfile](https://github.com/proof-media/rchain-notebook/tree/master/builds/notebooker))
