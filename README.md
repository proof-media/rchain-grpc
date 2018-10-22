
## rchain-grpc

| package | tests | updates |
| --- | --- | --- |
| [![image](https://img.shields.io/pypi/v/rchain-grpc.svg)](https://pypi.python.org/pypi/rchain-grpc) | [![image](https://travis-ci.com/proof-media/rchain-grpc.svg?branch=master)](https://travis-ci.com/proof-media/rchain-grpc) | [![Updates](https://pyup.io/repos/github/proof-media/rchain-grpc/shield.svg)](https://pyup.io/repos/github/proof-media/rchain-grpc/)

Python3 client for RChain nodes gRPC protocol

*   Free software: MIT license
*   Documentation: [https://proof-media.github.io/rchain-grpc](https://proof-media.github.io/rchain-grpc)

## Features

*   TODO

## Media

*   [Recorded walk-through](youtu.be/H_pmVff7c3Q) and [slides](https://nbviewer.jupyter.org/format/slides/github/proof-media/rchain-notebook/blob/master/notebooks/walk-through.ipynb#/) for the rchain discord community
*   [Notebook examples](https://github.com/proof-media/rchain-notebook) running on this [container image](https://hub.docker.com/r/proofmedia/rchain-notebook/) (see also [Dockerfile](https://github.com/proof-media/rchain-notebook/tree/master/builds/notebooker))

## Versions

* Releases <= `0.0.10` were compatible with `RNode 0.6.x`
* `0.0.11` is compatible with `RNode 0.7.x`
* `0.0.?` will be compatible with `RNode 0.8.x`


## Compiling

When a new version from RChain gets released,
protobuf definitions / descriptors must be updated.

This can be done selecting a new RNODE_RELEASE in env file
and running:

```bash
docker-compose run --rm generate
```

