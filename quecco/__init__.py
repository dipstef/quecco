import quelo
from .thread import connect as thread_connect
from .process import connect as process_connect


def _enum(**enums):
    return type('Enum', (), enums)


scope = _enum(local='local', threads='intra_process', processes='inter_process')

_connections = {scope.local: quelo.connect, scope.threads: thread_connect, scope.processes: process_connect}


def connect(path, init_file=None, scope=scope.local):
    conn = _connections[scope]
    return conn(path, init_file=init_file)


def get_connection(scope):
    return _connections[scope]