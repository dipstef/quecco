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

    from quecco import connect, threads, ipc

    with quecco.connect('test.db', scope=threads) as conn:
        ......


For statements to be executed from threads in different processes

.. code-block:: python

    import quecco

    with quecco.connect('test.db', scope=ipc) as conn:
        ......


Performance
===========
For the sake of comparison

executing 10000 times:

.. code-block:: sql
    select 1

.. code-block::

    Single Connection:   0.702931165695
    Threads Queue:       5.8118019104
    Process Queue:       10.071187973