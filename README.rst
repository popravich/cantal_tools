Cantal tools
============

High level tools for cantal metrics collection system.

:Documentation: ./docs
:Status: alpha

Basic usage:

.. code-block:: python

   import cantal
   import cantal_tools
   from cantal_tools.wsgi import CantaledWSGIServer

   metrics = cantal_tools.Metrics(__name__)
   cantal.start()

   CantaledWSGIServer(
       metrics=metrics,
       port=8080,
       ).serve_forever()

