.. Cantal Tools documentation master file, created by
   sphinx-quickstart on Mon Apr 18 09:49:21 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Cantal Tools's documentation!
========================================

High level tools for `cantal`_ metrics collection system.

Basic usage:

.. code-block:: python

   import cantal
   from cantal_tools.werkzeug_serving import CantaledWSGIServer

   cantal.start()

   CantaledWSGIServer(
       port=8080,
       ).serve_forever()

**Contents**:

.. toctree::
   :maxdepth: 3

   install
   metrics
   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _cantal: http://cantal-py.readthedocs.io
