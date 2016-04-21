.. Cantal Tools documentation master file, created by
   sphinx-quickstart on Mon Apr 18 09:49:21 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Cantal Tools's documentation!
========================================

High level tools for cantal metrics collection system.

:Documentation: 

.. include:: _latestpackage.rst

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

