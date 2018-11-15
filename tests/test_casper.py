import random
import secrets
from concurrent import futures

import pytest
from rchain_grpc import casper, exceptions


@pytest.fixture
def connection(rchain_host):
    with casper.create_connection(host=rchain_host) as conn:
        yield conn


@pytest.fixture
def block_fields():
    return {
        'blockHash',
        'blockSize',
        'blockNumber',
        'deployCount',
        'faultTolerance',
        'mainParentHash',
        'parentsHashList',
        'sender',
        'shardId',
        'tupleSpaceHash',
        'tupleSpaceDump',
        'timestamp',
        'version',
    }


@pytest.fixture
def rchain_ch_name():
    suffix = secrets.token_hex(5)
    return f'ch_name_{suffix}'


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


@pytest.fixture
def block_hash(connection):
    return casper.get_blocks(connection, depth=1).pop().get('blockHash')


def test_get_blocks(connection, block_fields):
    blocks = casper.get_blocks(connection, depth=100)
    assert isinstance(blocks, list)
    assert len(blocks) > 0
    for block in blocks:
        for field in block.keys():
            assert field in block_fields


def test_get_block(connection, block_hash, block_fields):
    block = casper.get_block(connection, block_hash)
    assert isinstance(block, dict)
    assert len(block) > 0
    for field in block.keys():
        assert field in block_fields


def test_deploy(deployed):
    assert deployed == {'message': 'Success!', 'success': True}


def test_propose(proposed):
    assert isinstance(proposed, dict)
    assert proposed['success'] is True
    assert 'created and added' in proposed['message']


def parse_output(ret):
    # TODO: test with channels with more data and figure out how to remove
    #       this nested list from here
    return ret['blockResults'][0]['postBlockData']


def test_get_value_from(proposed, rchain_ch_name, rchain_ch_value, connection):
    ret = casper.get_value_from(connection, rchain_ch_name)
    assert parse_output(ret)[0][0] == rchain_ch_value


def test_get_value_from_empty_channel(connection, rchain_ch_name):
    ret = casper.get_value_from(connection, f'not-{rchain_ch_name}')
    assert ret is None


def test_run_and_get_value_from(connection, rchain_ch_value):
    term = f'proof_output!("{rchain_ch_value}")'
    ret = casper.run_and_get_value_from(connection, term)
    assert parse_output(ret)[0][0] == rchain_ch_value


def test_listen_on(deployed, connection, rchain_ch_name, rchain_ch_value):
    def run():
        return next(casper.listen_on(connection, rchain_ch_name))

    with futures.ThreadPoolExecutor() as executor:
        future = executor.submit(run)
        casper.propose(connection)
        ret = future.result(timeout=5)
        assert parse_output(ret)[0][0] == rchain_ch_value


def test_listen_on_timeout_if_not_deployed_and_proposed(connection, rchain_ch_name):
    with pytest.raises(exceptions.TimeoutException):
        next(casper.listen_on(connection, rchain_ch_name, timeout=1))


@pytest.mark.parametrize(
    'args,expected',
    [
        ('true', [[True]]),
        ('false', [[False]]),
        ('1, false', [[1], [False]]),
        ('{}.set("x", 24).set("y", "value")', [[{'x': 24, 'y': 'value'}]]),
    ],
)
def test_value_conversion(args, expected, connection):
    term = f'proof_output!({args})'
    ret = casper.run_and_get_value_from(connection, term)
    assert parse_output(ret) == expected


@pytest.mark.parametrize("contract", ["add1", ["add", "1"]])
def test_run_contract(contract, connection, add_contract_path):
    number = random.randint(100, 1000)
    with open(add_contract_path) as contract_file:
        term = contract_file.read()
    casper.deploy(connection, term)
    casper.propose(connection)
    ret = casper.run_contract(connection, contract, [number])
    assert parse_output(ret)[0][0] == number + 1
