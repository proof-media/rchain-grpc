import secrets

import pytest

from rchain_grpc import casper


@pytest.fixture
def connection(rchain_host):
    return casper.create_connection(host=rchain_host)


def test_get_blocks(connection):
    blocks = casper.get_blocks(connection)
    fields = {
        'blockHash',
        'blockSize',
        'deployCount',
        'tupleSpaceHash',
        'tupleSpaceDump',
        'timestamp',
        'faultTolerance',
        'shardId',
    }
    assert isinstance(blocks, list)
    assert len(blocks) > 0
    for block in blocks:
        assert fields.issubset(set(block.keys()))


@pytest.fixture
def rchain_ch_name():
    sufix = secrets.token_hex(5)
    return f'ch_name_{sufix}'


@pytest.fixture
def rchain_ch_value():
    return secrets.token_hex(5)


@pytest.fixture
def deployed(connection, rchain_ch_name, rchain_ch_value):
    rho_term = f'@"{rchain_ch_name}"!("{rchain_ch_value}")'
    return casper.deploy(connection, rho_term)


@pytest.fixture
def proposed(connection, deployed):
    return casper.propose(connection)


def test_deploy(deployed):
    assert deployed == {'message': 'Success!', 'success': True}


def test_propose(proposed):
    assert isinstance(proposed, dict)
    assert proposed['success'] == True
    assert 'created and added' in proposed['message']


def test_get_value_from(proposed, rchain_ch_name, rchain_ch_value, connection):
    ret = casper.get_value_from(connection, rchain_ch_name)
    # TODO: test with channels with more data and figure out how to remove
    #       this nested list from here
    assert ret['blockResults'][0]['postBlockData'] == [[rchain_ch_value]]


def test_run_and_get_value_from(connection, rchain_ch_value):
    term = f'proof_output!("{rchain_ch_value}")'
    ret = casper.run_and_get_value_from(connection, term)
    assert ret['blockResults'][0]['postBlockData'] == [[rchain_ch_value]]
