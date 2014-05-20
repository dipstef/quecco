from quelo import statement


class CloseCursor(statement.CloseCursor):
    def __init__(self, cursor):
        self._cursor = cursor
        
    def __call__(self, conn):
        return super(CloseCursor, self).__call__(self._cursor)
    
    
class Execute(statement.Execute):
    def __init__(self, cursor, query, args):
        super(Execute, self).__init__(query, args)
        self._cursor = cursor
        
    def __call__(self, conn):
        return super(Execute, self).__call__(self._cursor)
    
    
class Select(statement.Select):
    def __init__(self, cursor, query, args):
        super(Select, self).__init__(query, args)
        self._cursor = cursor

    def __call__(self, conn):
        return super(Select, self).__call__(self._cursor)


class IterateSelect(statement.IterateSelect):
        
    def __init__(self, cursor, query, args, result_size=100):
        super(IterateSelect, self).__init__(query, args, result_size)
        self._cursor = cursor

    def __call__(self, conn):
        return super(IterateSelect, self).__call__(self._cursor)