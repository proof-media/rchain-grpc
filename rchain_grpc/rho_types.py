import functools
import json
from typing import Any, List, Tuple, TypeVar, Union

import toolz
from google.protobuf.empty_pb2 import Empty
from google.protobuf.internal.containers import (RepeatedCompositeFieldContainer,
                                                 RepeatedScalarFieldContainer)
from google.protobuf.message import Message

from .generated.CasperMessage_pb2 import DataWithBlockInfo
from .generated.RhoTypes_pb2 import Channel, Expr, Par, Var


def e_map_body_to_dict(body):
    kvs = body['kvs']
    ret = {}
    for kv in kvs:
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
def expr_from_obj(_: Any) -> None:
    raise ValueError(f'unknown type {type(_)}')


@expr_from_obj.register(str)
def _(s: str) -> Expr:
    return from_dict({'g_string': s}, Expr)


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


def from_dict(d: dict, klass: GrpcClass) -> GrpcClass:
    proto = klass()
    for key, value in d.items():
        setattr(proto, key, value)
    return proto


def to_channel(objs: list) -> Channel:
    par = Par()
    par.exprs.extend([expr_from_obj(obj) for obj in objs])
    channel = Channel()
    channel.quote.CopyFrom(par)
    return channel


@functools.singledispatch
def to_public_channel_name(other: Any):
    return f'@"{other}"'


@to_public_channel_name.register(list)
@to_public_channel_name.register(tuple)
def _(t: Union[List[Any], Tuple[Any]]):
    parts = ','.join([json.dumps(p) for p in t])
    return f'@[{parts}]'
