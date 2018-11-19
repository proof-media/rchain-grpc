
import json
import secrets
import time
from datetime import datetime
from typing import Any, Iterator, List, Optional

from google.protobuf.empty_pb2 import Empty

from . import rho_types
from .exceptions import CasperException, TimeoutException

from .generated.CasperMessage_pb2_grpc import DeployServiceStub
from .generated.CasperMessage_pb2 import (
    BlockQuery, BlocksQuery,
    PhloLimit, PhloPrice,
    DeployData,
)

from .utils import Connection, create_connection_builder, is_equal


# NOTE: default port for CASPER gRPC is 40401
create_connection = create_connection_builder(DeployServiceStub)


def throw_if_not_successful(response: dict, name: str) -> dict:
    if response.get('success') is not True:
        raise CasperException(f'Operation "{name}": not successfull', response)
    return response


def get_blocks(connection: Connection, depth: int = 1) -> List[dict]:
    """works in the same way as `./rnode show-blocks`"""
    output = connection.showBlocks(BlocksQuery(depth=depth))
    return [rho_types.to_dict(i) for i in output]


def get_block(connection: Connection, block_hash: str) -> dict:
    """works in the same way as `./rnode show-block HASH`"""
    output = connection.showBlock(
        BlockQuery(hash=block_hash)
    )
    return rho_types.to_dict(output).get('blockInfo')


def deploy(
    connection: Connection,
    term: str,
    from_: str = '0x0',
    phlo_limit: int = 10000000,
    phlo_price: int = 1,
    nonce: int = 0,
) -> dict:
    """works in the same way as `./rnode deploy`
    but expect contract code in `term` argument"""
    dt = datetime.now()
    timestamp = dt.microsecond
    deployData = rho_types.from_dict(
        {
            'term': term,
            'from': from_,
            'phloLimit': PhloLimit(value=phlo_limit),
            'phloPrice': PhloPrice(value=phlo_price),
            'nonce': nonce,
            'timestamp': timestamp,
        },
        DeployData,
    )

    output = connection.DoDeploy(deployData)
    return throw_if_not_successful(rho_types.to_dict(output), 'deploy')


def propose(connection: Connection) -> dict:
    """works in the same way as `./rnode propose`"""
    output = connection.createBlock(Empty())
    return throw_if_not_successful(rho_types.to_dict(output), 'propose')


def listen_on(
    connection: Connection, name: str, interval: float = 0.5, timeout: float = 60.0
) -> Iterator[dict]:
    ""
    """listen on channel and return iterator witch values.
    Check channel in every second given in `interval`"""
    old_value = {}

    # TODO: ask rchain dev team for making `showBlocks` streaming infinitely
    # TODO: use infinite stream from `showBlocks` instead and check only on new block
    start_time = time.time()
    while True:
        value = get_value_from(connection, name)
        if value is not None and not is_equal(value, old_value):
            yield value
            old_value = value
        if time.time() - start_time + interval > timeout:
            raise TimeoutException()
        time.sleep(interval)


def get_value_from(connection: Connection, name: str) -> Optional[dict]:
    """get value from channel on given name"""
    rchain_channel = rho_types.to_channel([name])
    output = connection.listenForDataAtName(rchain_channel)
    # from google.protobuf.json_format import MessageToDict
    # result = MessageToDict(output)
    # print(result)
    result = rho_types.to_dict(output)
    if 'blockResults' in result:
        return result
    return None


def run_and_get_value_from(
    connection: Connection,
    term: str,
    output_placeholder: str = 'proof_output',
    **deploy_kargs,
) -> dict:
    """function deploy and propose given term and if in term is used channel
    `proof_output` (eg. `proof_output!("hello")`") will listen on, replace this
    name with the internal channel and start listening on this. Name of this
    channel can be configured by `output_placeholder`. Rest of kargs will be
    passed to `deploy` function."""

    channel_name = f'rchain_grpc_{secrets.token_hex(5)}'
    channel_name_str = rho_types.to_public_channel_name(channel_name)
    preprocessed_term = term.replace(output_placeholder, channel_name_str)
    deploy(connection, preprocessed_term, **deploy_kargs)
    propose(connection)
    return get_value_from(connection, channel_name)


def run_contract(
    connection: Connection,
    contract_name: str,
    contract_args: List[Any],
    timeout: float = 60.0,
    **deploy_kwargs,
):
    """
    Run contract and return result if contract accept callback channel as last argument:
    ```rholang
    contract @"add1"(@number, cb) = {
      cb!(number + 1)
    }
    ```
    """
    ack_name = f'ack_{secrets.token_hex(10)}'
    ack_name_str = rho_types.to_public_channel_name(ack_name)
    contract_name_str = rho_types.to_public_channel_name(contract_name)
    contract_args_str = ', '.join(
        [json.dumps(a) for a in contract_args] + [f'*{ack_name_str}']
    )
    term = f'{contract_name_str}!({contract_args_str})'

    deploy(connection, term, **deploy_kwargs)
    propose(connection)
    return next(listen_on(connection, ack_name, timeout=timeout))
