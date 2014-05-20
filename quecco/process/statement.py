from quelo import statement


class CursorId(statement.ConnectionStatement):

    def _execute_statement(self, conn):
        return conn.create_cursor()

    def __repr__(self):
        return 'conn.cursor()'


class CloseCursor(statement.CloseCursor):
    def __init__(self, cursor_id):
        self._cursor_id = cursor_id
        
    def __call__(self, conn):
        cursor = conn.get_cursor(self._cursor_id)

        return super(CloseCursor, self).__call__(cursor)
    
    
class Execute(statement.Execute):
    def __init__(self, cursor_id, query, args):
        super(Execute, self).__init__(query, args)
        self._cursor_id = cursor_id
        
    def __call__(self, conn):
        cursor = conn.get_cursor(self._cursor_id)

        return super(Execute, self).__call__(cursor)
    
    
class Select(statement.Select):
    def __init__(self, cursor_id, query, args):
        super(Select, self).__init__(query, args)
        self._cursor_id = cursor_id

    def __call__(self, conn):
        cursor = conn.get_cursor(self._cursor_id)

        return super(Select, self).__call__(cursor)


class IterateSelect(statement.IterateSelect):
        
    def __init__(self, cursor_id, query, args, result_size=100):
        super(IterateSelect, self).__init__(query, args, result_size)
        self._cursor_id = cursor_id

    def __call__(self, conn):
        cursor = conn.get_cursor(self._cursor_id)

        return super(IterateSelect, self).__call__(cursor)