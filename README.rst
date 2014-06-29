Quecco
======

A concurrent ``sqlite3`` interface based on ``quelo``


Features
========

A ``sqlite3`` connection can only be used in the same thread has been created, thus querying a database from other
threads or processes is not possible.
This limitation can be overcome by using a producer-consumer queue, where multiple consumers requests results of
operations executed by the producer.

In this the consumer are threads/processes requesting for database statements to be executed and the producer is
the same thread that has initiated a ``sqlite3`` connection


Usage
=====
Same interface as ``quelo``, see the quelo documentation at https://github.com/dipstef/quelo.

For statements to be executed from threads in the same process

.. code-block:: python

    import quecco

    with quecco.connect('test.db', scope=quecco.threads) as conn:
        ......


For statements to be executed from threads in different processes

.. code-block:: python

    import quecco

    with quecco.connect('test.db', scope=quecco.ipc) as conn:
        ......

