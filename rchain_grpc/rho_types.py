import functools
import json
from typing import Any, List, Tuple, TypeVar, Union

import toolz
from google.protobuf.message import Message

from ._grpc_containers import (RepeatedCompositeFieldContainer,
                               RepeatedScalarFieldContainer)

# TODO: please check, but without it doesn't work
from google.protobuf.pyext._message import \
    RepeatedCompositeContainer, RepeatedScalarContainer

from .generated.RhoTypes_pb2 import Expr, Par
from .generated.CasperMessage_pb2 import DataAtNameQuery


def e_map_body_to_dict(body):
    ret = {}
    for kv in body['kvs']:
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
    # print("Who am I?", other, type(other))
    return other


# TODO: please check, but without it doesn't work
@to_dict.register(RepeatedCompositeContainer)
def _(container: RepeatedCompositeContainer) -> List[dict]:
    return [to_dict(e) for e in container]


# TODO: please check, but without it doesn't work
@to_dict.register(RepeatedScalarContainer)
def _(container: RepeatedScalarContainer) -> List[dict]:
    return [to_dict(e) for e in container]


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


def from_dict(d: dict, grpc_class: GrpcClass) -> GrpcClass:
    # TODO: check if this can be removed
    return grpc_class(**d)


@functools.singledispatch
def expr_from_obj(_: Any) -> None:
    raise ValueError(f'unknown type {type(_)}')


@expr_from_obj.register(str)
def _(s: str) -> Expr:
    return from_dict({'g_string': s}, Expr)


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
