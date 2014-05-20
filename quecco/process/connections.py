from contextlib import closing


class DbConnections(object):

    def __init__(self, connections):
        self._connections = connections
        self._databases = {}

    def connect(self, database, **kwargs):
        database = self._get_database(database)

        return database.connect(**kwargs)

    def _get_database(self, database):
        try:
            return self._databases[database]
        except KeyError:
            self._databases[database] = Database(database, self._get_db_connection(database))
            return self._databases[database]

    def _get_db_connection(self, database):
        try:
            return self._connections[database]
        except KeyError:
            raise UnsupportedDatabase(database)

    def get_connection(self, database, connection_id):
        db = self._get_database(database)

        return db.get_connection(connection_id)

    def close_connection(self, database, connection_id):
        db = self._get_database(database)
        db.close(connection_id)

    def close(self):
        for database in self._databases.values():
            database.close_connections()


class Database(object):
    def __init__(self, name, connection):
        self._name = name
        self._connection = connection
        self._connections = {}

    def connect(self, **kwargs):
        if not self._connections:
            conn = DatabaseConnection(self._name, self._connection(**kwargs))
            self._connections[conn.id] = conn
        else:
            conn = self._connections.values()[0]

        return conn

    def get_connection(self, connection_id):
        try:
            return self._connections[int(connection_id)]
        except KeyError:
            raise ConnectionNotFound()

    def close_connections(self):
        for conn in self._connections.values():
            self._close_connection(conn)

    def close_connection(self, connection_id):
        connection = self.get_connection(connection_id)
        self._close_connection(connection)

    def _close_connection(self, conn):
        conn.close()
        del self._connections[conn.id]


class Connection(closing):

    def __init__(self, conn):
        super(Connection, self).__init__(self)
        self._conn = conn
        self._cursors = {}

    def commit(self):
        self._conn.commit()

    def create_cursor(self):
        cursor = self._conn.cursor()

        cursor_id = id(cursor)
        self._cursors[cursor_id] = cursor

        return cursor_id

    def executescript(self, script):
        self._conn.executescript(script)

    def get_cursor(self, cursor_id):
        try:
            return self._cursors[int(cursor_id)]
        except KeyError:
            raise CursorNotFound()

    def close_cursor(self, cursor_id):
        cursor = self.get_cursor(cursor_id)
        cursor.close()
        del self._cursors[int(cursor_id)]

    def close(self):
        for cursor_id in self._cursors.keys():
            self.close_cursor(cursor_id)
        self._conn.close()


class DatabaseConnection(Connection):

    def __init__(self, database, conn):
        super(DatabaseConnection, self).__init__(conn)
        self.database = database
        self.id = 1


class UnsupportedDatabase(Exception):

    def __init__(self, database):
        super(UnsupportedDatabase, self).__init__()
        self._database = database

    def __str__(self):
        return 'Unsupported database: %s' % self._database


class ConnectionNotFound(Exception):
    def __init__(self, *args, **kwargs):
        super(ConnectionNotFound, self).__init__(*args, **kwargs)


class CursorNotFound(Exception):
    def __init__(self, *args, **kwargs):
        super(CursorNotFound, self).__init__(*args, **kwargs)