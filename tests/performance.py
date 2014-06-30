from contextlib import closing
import timeit
import quecco
from quelo import get_value


def _select_number(connection, number):
    with closing(connection.cursor()) as cursor:
        result = get_value(cursor, '''select ?''', (number, ))
        return result
    

def serial_test(conn, numbers=10, times=1):
    def _serial_test():
        for i in xrange(1, numbers + 1):
            r = _select_number(conn, i)
            assert r == i

    return timeit.timeit(_serial_test, number=times)


def test(times=100):
    with quecco.local('test.db', init_file='test.sql') as conn:
        print 'Local: ', serial_test(conn, times=times)

    with quecco.threads('test.db', init_file='test.sql') as conn:
        print 'Threads: ', serial_test(conn, times=times)

    with quecco.ipc('test.db', init_file='test.sql') as conn:
        print 'Ipc: ', serial_test(conn, times=times)

if __name__ == '__main__':
    test(times=1000)