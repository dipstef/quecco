from quelo.query import get_value

from softarchive.contrib.db.connection.sqlite import db_cursor
from quecco import thread, process
from tests import TestDatabaseConnection


def _test_connections(connect):
    connection = TestDatabaseConnection(connect)

    conn1 = connection()
    conn2 = connection()

    with db_cursor(conn1) as cursor1:
        cursor1.execute('''create table if not exists test (value integer primary key not null)''')

        cursor1.execute('''delete from test''')
        conn1.commit()

        cursor1.execute('''insert into test(value)
                                  values(?) ''', (1, ))
        conn1.commit()
    with db_cursor(conn2) as cursor2:
        value = get_value(cursor2, '''select value
                                        from test
                                       where value = ?''', (1, ))

        assert value == 1
        if not value:
            cursor2.execute('''insert into test(value)
                                      values(?) ''', (1, ))
    conn1.close()
    conn2.close()


def main():

    _test_connections(thread.connect)
    _test_connections(process.connect)

if __name__ == '__main__':
    main()