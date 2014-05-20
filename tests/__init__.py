import atexit
import os


class TestDatabaseConnection(object):

    def __init__(self, connect):
        self._connect = connect
        self._path = os.path.join(os.path.dirname(__file__), 'test.db')
        atexit.register(self._remove_path)

    def __call__(self):
        return self._connect(self._path)

    def __exit__(self, *args):
        self._remove_path()

    def _remove_path(self):
        if os.path.exists(self._path):
            os.remove(self._path)