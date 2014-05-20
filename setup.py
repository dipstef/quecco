from distutils.core import setup

VERSION = '0.1'

desc = """Extending the use of a a sqlite connection concurrently using (thread, processes) queue
or through file locking"""

name = 'quecco'

setup(name=name,
      version=VERSION,
      author='Stefano Dipierro',
      author_email='dipstef@github.com',
      url='http://github.com/dipstef/{}/'.format(name),
      description=desc,
      packages = ['quecco', 'quecco.process', 'quecco.thread'],
      platforms=['Any'],
      requires=['quelo']
)