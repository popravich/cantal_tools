Cantal tools
============

High level tools for `cantal`_ metrics collection system.

Documentation: http://cantal-tools.readthedocs.io

Package contains utils for collecting metrics for
WSGI applications, Flask, Redis, Elasticsearch, SQLAlchemy and Django.
See docs for more.

Basic usage:

.. code-block:: python

   import cantal
   from cantal_tools.werkzeug_serving import CantaledWSGIServer

   cantal.start()

   CantaledWSGIServer(
       port=8080,
       ).serve_forever()

.. _cantal: http://cantal-py.readthedocs.io
