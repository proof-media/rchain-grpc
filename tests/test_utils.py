from unittest import mock

import pytest

from rchain_grpc import utils
from rchain_grpc.exceptions import ConnectionClosedException


@pytest.fixture
def stub():
    s = mock.MagicMock()
    s.test_method.return_value = 22
    return s


@pytest.fixture
def channel():
    return mock.MagicMock()


@pytest.fixture
def connection(channel, stub):
    return utils.create_connection(lambda _: stub, channel_fn=lambda _: channel)


def test_connection_works_as_proxy_to_stub(channel, stub, connection):
    args = [1, '2']
    value = 'test value'

    ret = connection.test_method(*args)
    assert ret == 22
    stub.test_method.assert_called_once_with(*args)

    connection.value = value
    assert stub.value == value


def test_connection_as_contextmanager(channel, stub, connection):
    with connection as connection_from_context_manager:
        ret = connection_from_context_manager.test_method(1)
        assert ret == 22
        assert isinstance(connection_from_context_manager, utils.Connection)
        assert connection_from_context_manager is connection
    with pytest.raises(ConnectionClosedException):
        connection.test_method(1)
