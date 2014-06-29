import quelo
from .thread import connect as thread_connect
from .process import connect as process_connect


local = quelo.connect
threads = thread_connect
ipc = process_connect


class Connections(object):
    local = local
    threads = threads
    ipc = ipc

scope = Connections()


def connect(path, init_file=None, scope=scope.local):
    return scope(path, init_file=init_file)