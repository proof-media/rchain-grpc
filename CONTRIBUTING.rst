
============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/proof-media/rchain_grpc/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

rchain-grpc could always use more documentation, whether as part of the
official rchain-grpc docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/proof-media/rchain_grpc/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `rchain_grpc` for local development.

1. Fork the `rchain_grpc` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/rchain_grpc.git

3. Install docker and docker-compose
4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that they pass tests::

    $ ./test_all_python_versions.sh

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.7
   https://travis-ci.org/proof-media/rchain_grpc/pull_requests
   and make sure that the tests pass for all supported Python versions.


Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run::

$ bumpversion patch # possible: major / minor / patch
$ git push
$ git push --tags

Travis will then deploy to PyPI if tests pass.


Upgrading to new RNode release
---------

When a new version from RChain gets released,
protobuf definitions / descriptors must be updated/re-compiled.

This can be done selecting a new RNODE_RELEASE in the .env file
and then running::

    $ docker-compose run --rm generate


Debugging
---------

You can access a working shell on docker with::

    $ docker-compose run --rm --entrypoint /bin/bash tests-37
    $ pip install ipython && pip install --editable . && ipython
    # [ipython shell]


Or run tests in watch mode:

    $ docker-compose run --rm tests-37 watch
