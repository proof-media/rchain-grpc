class GRPCException(Exception):
    pass


class CasperException(GRPCException):
    pass


class ConnectionClosedException(GRPCException):
    pass


class TimeoutException(GRPCException):
    pass
