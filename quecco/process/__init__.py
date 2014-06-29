from contextlib import closing
from procol.queue.ipc import ProducerConsumer
from quelo.sqlite import DbConnection, sqlite_connect
from quelo.sqlite.connect import DbPathConnect

from .connections import Connection
from ..queue import ConnectionStatementsThread
from .statement import CursorId, Execute, Select, IterateSelect, CloseCursor


class DbConnectionMultiProcessing(DbConnection):
    def __init__(self, path):
        super(DbConnectionMultiProcessing, self).__init__()
        self._queue = DbConnectionProcess(path)
        self._queue.start()

    def cursor(self):
        cursor_id = self._execute(CursorId())
        return MultiProcessCursor(cursor_id, self._queue)

    def close(self):
        self._queue.close()

    def _execute(self, statement):
        return self._queue.execute(statement)


class MultiProcessCursor(closing):

    def __init__(self, cursor_id, queue):
        super(MultiProcessCursor, self).__init__(self)
        self._cursor_id = cursor_id
        self._queue = queue

    def execute(self, query, args=None):
        return self._execute(Execute(self._cursor_id, query, args))

    def select(self, query, args=None):
        return self._execute(Select(self._cursor_id, query, args))

    def iterate_select(self, query, args=None, result_size=100):
        return self._execute(IterateSelect(self._cursor_id, query, args, result_size=result_size))

    def close(self):
        return self._execute(CloseCursor(self._cursor_id))

    def _execute(self, statement):
        return self._queue.execute(statement)


class Sqlite3Connection(Connection):
    def __init__(self, path):
        super(Sqlite3Connection, self).__init__(sqlite_connect(path))


class DbConnectionProcess(ConnectionStatementsThread):
    def __init__(self, path):
        self.path = path
        super(DbConnectionProcess, self).__init__(statements_queue=ProducerConsumer())

    def _connect(self):
        return Sqlite3Connection(self.path)


connect = DbPathConnect(DbConnectionMultiProcessing)