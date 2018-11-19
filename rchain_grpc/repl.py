from . import rho_types
from .generated import repl_pb2_grpc
from .generated.repl_pb2 import CmdRequest, EvalRequest
from .utils import Connection, create_connection_builder

# NOTE: default port for REPL is 40402
create_connection = create_connection_builder(repl_pb2_grpc.ReplStub)


def run(connection: Connection, line: str) -> dict:
    cmd_request = rho_types.from_dict({'line': line}, CmdRequest)
    ret = connection.Run(cmd_request)
    return rho_types.to_dict(ret)


def eval(connection: Connection, program: str) -> dict:
    eval_request = rho_types.from_dict({'program': program}, EvalRequest)
    ret = connection.Eval(eval_request)
    return rho_types.to_dict(ret)
