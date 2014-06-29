import quelo
from .thread import connect as thread_connect
from .process import connect as process_connect


local = quelo.connect
threads = thread_connect
ipc = process_connect


class Connection(object):
    local = local
    in_process = threads
    ipc = ipc

connection = Connection


def connect(path, init_file=None, scope=connection.local):
    return scope(path, init_file=init_file)