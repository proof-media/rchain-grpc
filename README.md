
## rchain-grpc

| package | tests | updates |
| --- | --- | --- |
| [![image](https://img.shields.io/pypi/v/rchain-grpc.svg)](https://pypi.python.org/pypi/rchain-grpc) | [![image](https://travis-ci.com/proof-media/rchain-grpc.svg?branch=master)](https://travis-ci.com/proof-media/rchain-grpc) | [![Updates](https://pyup.io/repos/github/proof-media/rchain-grpc/shield.svg)](https://pyup.io/repos/github/proof-media/rchain-grpc/)

Python3 client for RChain nodes gRPC protocol

*   Free software: MIT license
*   Documentation: [https://proof-media.github.io/rchain-grpc](https://proof-media.github.io/rchain-grpc)


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


## Other media

*   [Recorded walk-through](youtu.be/H_pmVff7c3Q) and [slides](https://nbviewer.jupyter.org/format/slides/github/proof-media/rchain-notebook/blob/master/notebooks/walk-through.ipynb#/) for the rchain discord community
*   [Notebook examples](https://github.com/proof-media/rchain-notebook) running on this [container image](https://hub.docker.com/r/proofmedia/rchain-notebook/) (see also [Dockerfile](https://github.com/proof-media/rchain-notebook/tree/master/builds/notebooker))
