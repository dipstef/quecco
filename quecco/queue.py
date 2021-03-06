from threading import Thread
from procol.queue import RequestsClosed
from quelo.error import DbError


class ConnectionStatementsThread(Thread):

    def __init__(self, statements_queue):
        super(ConnectionStatementsThread, self).__init__(target=self._execute_statements)
        self._statements = statements_queue

    def _execute_statements(self):
        with self._connect() as conn:
            statements = self._statements.requests()
            for statement in statements:
                try:
                    result = (True, statement(conn))
                except BaseException, e:
                    result = (False, e)
                statements.send(result)

    def _connect(self):
        raise NotImplementedError

    def _send_result(self, result):
        self._statements.add_result(result)

    def execute(self, statement):
        try:
            completed, result = self._statements.execute(statement)
            if not completed:
                raise result
            return result
        except RequestsClosed:
            raise DbError('Database Connection already closed can not perform: %s' % statement)

    def close(self):
        self._statements.close()