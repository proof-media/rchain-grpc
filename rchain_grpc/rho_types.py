import functools
import json
from typing import Any, List, Tuple, TypeVar, Union

import toolz

# from google.protobuf.empty_pb2 import Empty
# from .generated.CasperMessage_pb2 import DataWithBlockInfo
from google.protobuf.message import Message
from ._grpc_containers import (RepeatedCompositeFieldContainer,
                               RepeatedScalarFieldContainer)
# from .generated.RhoTypes_pb2 import Channel, Par, Var
from .generated.RhoTypes_pb2 import Expr, Par
from .generated.CasperMessage_pb2 import DataAtNameQuery


def e_map_body_to_dict(body):
    ret = {}
    for kv in body.get('kvs'):
        k = toolz.get_in(['key', 0], kv)
        v = toolz.get_in(['value', 0], kv)
        ret[k] = v
    return ret


expr_to_obj_mapping = {'g_string': str, 'e_map_body': e_map_body_to_dict}

GrpcClass = TypeVar('GrpcClass')


def expr_to_obj(expr: dict) -> dict:
    type_, value = toolz.first(expr.items())
    return expr_to_obj_mapping.get(type_, toolz.identity)(value)


@functools.singledispatch
def to_dict(other: Any) -> Any:
    return other


@to_dict.register(RepeatedCompositeFieldContainer)
def _(container: RepeatedCompositeFieldContainer) -> List[dict]:
    return [to_dict(e) for e in container]


@to_dict.register(RepeatedScalarFieldContainer)
def _(container: RepeatedScalarFieldContainer) -> List[dict]:
    return [to_dict(e) for e in container]


@to_dict.register(Message)
def _(message: Message) -> dict:
    exprs = getattr(message, 'exprs', None)
    if exprs is not None:
        return [expr_to_obj(expr) for expr in to_dict(exprs)]
    return {f[0].name: to_dict(f[1]) for f in message.ListFields()}


@functools.singledispatch
def expr_from_obj(_: Any) -> None:
    raise ValueError(f'unknown type {type(_)}')


@expr_from_obj.register(str)
def _(s: str) -> Expr:
    return from_dict({'g_string': s}, Expr)


def from_dict(d: dict, grpc_class: GrpcClass) -> GrpcClass:
    # TODO: check me again

    ##########
    # OLD WAY
    # proto = grpc_class()
    # for key, value in d.items():
    #     setattr(proto, key, value)
    ##########
    # NEW WAY
    proto = grpc_class(**d)
    # print('From dict', proto)

    return proto


def to_channel(objs: list) -> DataAtNameQuery:
    par = Par()
    par.exprs.extend([expr_from_obj(obj) for obj in objs])
    channel = DataAtNameQuery(depth=1, name=par)
    return channel


@functools.singledispatch
def to_public_channel_name(other: Any):
    return f'@"{other}"'


@to_public_channel_name.register(list)
@to_public_channel_name.register(tuple)
def _(t: Union[List[Any], Tuple[Any]]):
    parts = ','.join([json.dumps(p) for p in t])
    return f'@[{parts}]'
