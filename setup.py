#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup_requirements = ['pytest-runner']

test_requirements = ['pytest']

setup(
    author="Mateusz Probachta",
    author_email='mateusz@proofmedia.io',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
    ],
    description="python client to rchain gRPC",
    entry_points={'console_scripts': ['py_rchain_grpc=rchain_grpc.cli:main']},
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='rchain_grpc',
    name='rchain_grpc',
    packages=find_packages(include=['rchain_grpc']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/proof-media/rchain-grpc',
    version='0.7.2',
    zip_safe=True,
)
