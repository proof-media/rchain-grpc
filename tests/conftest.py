import pytest
import os


@pytest.fixture
def rchain_host():
    return os.environ.get('RCHAIN_GRPC_HOST')
