import pytest
from rchain_grpc import repl


def verify_repl_output(repl_output):
    assert isinstance(repl_output, dict)
    tuple_space, costs = repl.output_parser(repl_output)
    assert 'Cost' in costs
    for keyword in ['Unforgeable', 'for', 'Nil']:
        keyword in tuple_space


@pytest.fixture
def connection(rchain_host):
    return repl.create_connection(host=rchain_host, port=40402)


def test_run(connection):
    ret = repl.run(connection, 'new x in { x!(1 + 1) }')
    verify_repl_output(ret)


def test_eval(connection):
    rholang_code = '''new stdout(`rho:io:stdout`) in {stdout!("testing!")}'''
    ret = repl.eval(connection, rholang_code)
    verify_repl_output(ret)
