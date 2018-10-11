import os

import pytest

ROOT = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def rchain_host():
    return os.environ.get('RCHAIN_GRPC_HOST')


@pytest.fixture
def add_contract_path():
    return os.path.join(ROOT, 'add1.rho')
