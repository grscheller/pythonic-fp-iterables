.. Pythonic FP - Circular Array documentation master file, created by
   sphinx-quickstart on Fri Jun 27 11:13:22 2025.
   To regenerate the documentation do: ``$ Sphinx-build -M html docs/source/ docs/build/``
   from the root repo directory.

Pythonic FP - Iterables project
===============================

Part of of the `pythonic-fp namespace projects <https://github.com/grscheller/pythonic-fp/blob/main/README.md>`_.

Overview
--------

PyPI project `pythonic.iterables <https://pypi.org/project/pythonic-fp.iterables/>`_
implementing a Python package of tools for iterables and iterators.

- Concatenating and merging iterables
- Dropping and taking values from iterables
- Reducing and accumulating iterables
- Assumptions
   
  - iterables are not necessarily iterators
  - at all times iterator protocol is assumed to be followed
     
    - all iterators are assumed to be iterable
    - for all iterators `my_iter` we assume `iter(my_iter) is my_iter`

Documentation
-------------

:doc:`Installation <installing>`
    Installing and importing the module.

:doc:`API docs <api>`
    Detailed API documentation.

Development
-----------

:doc:`changelog`
    CHANGELOG for the current and predecessor projects.

.. Hidden TOCs

.. toctree::
   :caption: Documentation
   :maxdepth: 2
   :hidden:

   installing
   api

.. toctree::
   :caption: Development
   :maxdepth: 2
   :hidden:

   changelog

