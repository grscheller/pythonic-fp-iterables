..
   Pythonic FP - Iterables documentation master file. To regenerate the sphinx
   documentation do: "$ make html" from the "docs/" directory.

Pythonic FP - Iterables
=======================

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

Part of of the
`pythonic-fp namespace projects <https://github.com/grscheller/pythonic-fp/blob/main/README.md>`_.

Documentation
-------------

:doc:`Installation <installing>`
    Installing and importing the module.

:doc:`API docs <api>`
    Detailed API documentation.

Development
-----------

:doc:`Current Development API <api>`
    Development environment API documentation.

:doc:`CHANGELOG <changelog>`
    For the current and predecessor projects.

.. toctree::
   :caption: Documentation
   :maxdepth: 2
   :hidden:

   installing
   api_pypi
   api

.. toctree::
   :caption: Development
   :maxdepth: 1
   :hidden:

   changelog

.. toctree::
   :caption: Back to start
   :maxdepth: 1
   :hidden:

   self
