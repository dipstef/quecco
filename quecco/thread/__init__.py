from contextlib import closing
from procol.queue.threads import ProducerConsumer
from quelo.sqlite import sqlite_connect, DbConnection
from quelo.sqlite.connect import DbPathConnect
from quelo.statement import Cursor
from ..queue import ConnectionStatementsThread

from .statement import Execute, Select, IterateSelect, CloseCursor


class DbConnectionThread(ConnectionStatementsThread):
    def __init__(self, path):
        super(DbConnectionThread, self).__init__(statements_queue=ProducerConsumer())
        self.path = path

    def _connect(self):
        return sqlite_connect(self.path)


class DbCursorThread(closing):

    def __init__(self, cursor, queue):
        super(DbCursorThread, self).__init__(self)
        self._cursor = cursor
        self._queue = queue

    def execute(self, query, args=None):
        return self._execute(Execute(self._cursor, query, args))

    def select(self, query, args=None):
        return self._execute(Select(self._cursor, query, args))

    def iterate_select(self, query, args=None, result_size=100):
        return self._execute(IterateSelect(self._cursor, query, args, result_size=result_size))

    def close(self):
        return self._execute(CloseCursor(self._cursor))

    def _execute(self, statement):
        return self._queue.execute(statement)


class DbConnectionMultiThread(DbConnection):
    def __init__(self, path):
        super(DbConnectionMultiThread, self).__init__()
        self._queue = DbConnectionThread(path)
        self._queue.start()

    def cursor(self):
        cursor = self._execute(Cursor())
        return DbCursorThread(cursor, self._queue)

    def close(self):
        self._queue.close()

    def _execute(self, statement):
        return self._queue.execute(statement)

connect = DbPathConnect(DbConnectionMultiThread)