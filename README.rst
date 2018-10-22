===========
rchain-grpc
===========


.. image:: https://img.shields.io/pypi/v/rchain-grpc.svg
    :target: https://pypi.python.org/pypi/rchain-grpc

.. image:: https://travis-ci.com/proof-media/rchain-grpc.svg?branch=master
    :target: https://travis-ci.com/proof-media/rchain-grpc

.. image:: https://readthedocs.org/projects/rchain-grpc/badge/?version=latest
    :target: https://rchain-grpc.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


.. image:: https://pyup.io/repos/github/proof-media/rchain-grpc/shield.svg
    :target: https://pyup.io/repos/github/proof-media/rchain-grpc/
    :alt: Updates



python client to rchain gRPC


* Free software: MIT license
* Documentation: https://rchain-grpc.readthedocs.io.


Features
--------

* TODO

Versioning
--------

* 0.0.10 is compatible with RNode 0.6.x
* 0.0.11 will be compatible with RNode 0.7.x

Upgrading gRPC client descriptors
-------

When a new version from RChain gets released,
protobuf definitions / descriptors must be updated.

This can be done selecting a new RNODE_RELEASE in env file
and running:

.. code:: bash

   docker-compose run --rm generate


Credits
-------

The source code we have here was inspired by the official snippet at:
https://github.com/rchain/rchain/tree/dev/node-client
