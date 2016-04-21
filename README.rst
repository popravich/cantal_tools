Cantal tools
============

High level tools for cantal metrics collection system.

:Documentation: http://cantal_tools.readthedocs.org
:Status: alpha

Basic usage:

.. code-block:: python

   import cantal
   from cantal_tools.werkzeug import CantaledWSGIServer

   cantal.start()

   CantaledWSGIServer(
       port=8080,
       ).serve_forever()

