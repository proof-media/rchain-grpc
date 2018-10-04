import secrets

import pytest

from rchain_grpc import repl


@pytest.fixture
def connection(rchain_host):
    return repl.create_connection(host=rchain_host)


@pytest.fixture
def contract_path():
    # file must be available from rchain container
    # look on `proof-monorepo/rchain` directory which is available
    # in rchain container on `/rchain` path.
    # It already has `test_contract.rho`
    return '/rchain/test_contract.rho'


@pytest.mark.xfail(reason='not work with current rnode')
def test_run(connection):
    ret = repl.run(connection, 'new x in { x!(1 + 1) }')
    assert isinstance(ret, dict)


@pytest.mark.xfail(reason='not work with current rnode')
def test_eval(connection, contract_path):
    ret = repl.eval(connection, contract_path)
    assert isinstance(ret, dict)
