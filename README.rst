
===========
rchain-grpc
===========


.. image:: https://img.shields.io/pypi/v/rchain-grpc.svg
    :target: https://pypi.python.org/pypi/rchain-grpc

.. image:: https://travis-ci.com/proof-media/rchain-grpc.svg?branch=master
    :target: https://travis-ci.com/proof-media/rchain-grpc

.. image:: https://pyup.io/repos/github/proof-media/rchain-grpc/shield.svg
    :target: https://pyup.io/repos/github/proof-media/rchain-grpc/
    :alt: Updates



Python3 client for RChain nodes gRPC protocol


* Free software: MIT license
* Documentation: https://proof-media.github.io/rchain-grpc


Features
--------

* TODO

Versioning
--------

* 0.0.10 was compatible with RNode 0.6.x
* 0.0.11 is be compatible with RNode 0.7.x
* 0.0.? will be compatible with RNode 0.8.x

Media
-----

-  `Recorded walk-through`_ and `slides`_ for the rchain discord
   community
-  `Notebook examples`_ running on this `container image`_ (see also
   `Dockerfile`_)

.. _Recorded walk-through: youtu.be/H_pmVff7c3Q
.. _slides: https://nbviewer.jupyter.org/format/slides/github/proof-media/rchain-notebook/blob/master/notebooks/walk-through.ipynb#/
.. _Notebook examples: https://github.com/proof-media/rchain-notebook
.. _container image: https://hub.docker.com/r/proofmedia/rchain-notebook/
.. _Dockerfile: https://github.com/proof-media/rchain-notebook/tree/master/builds/notebooker

Compiling
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
