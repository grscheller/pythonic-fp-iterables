=================================
Pythonic FP - Tools for iterables
=================================

Tools to create iterators from iterables, part of the
`PyPI pythonic-fp Namespace Projects <https://github.com/grscheller/pythonic-fp/blob/main/README.rst>`_.

Detailed API documentation
`documentation <https://grscheller.github.io/pythonic-fp/maintained/iterables>`_
on *GH-Pages*.

Features:
---------

- Concatenating and merging iterables
- Dropping and taking values from iterables
- Reducing and accumulating iterables
- Assumptions
  - iterables are not necessarily iterators
  - at all times iterator protocol is assumed to be followed
    - all iterators are assumed to be iterable
    - for all iterators `my_iter` we assume `iter(my_iter) is my_iter`

Functions to merge iterables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- concat: concatenate multiple iterables sequentially
- exhaust: shuffle together multiple iterables until all are exhausted
- merge: shuffle together multiple iterables until one is exhausted

Dropping and taking
^^^^^^^^^^^^^^^^^^^^

==================== ============================================
function             return iterator yielding values from ds
==================== ============================================
drop(ds, n)          with first n values of ds dropped
drop_while(ds, pred) dropping values until predicate false 
take(ds, n)          yielding first n values of ds
take_while(ds, pred) yielding values from ds while predicate true
==================== ============================================

========================== ========================================================
function                   return a pair of iterators
========================== ========================================================
take_split(ds, n)          like take but second iterator yields remaining values
take_while_split(ds, pred) like take_while, second iterator yields remaining values 
========================== ========================================================

Functions to accumulate and reduce
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- accumulate: pure Python version of std library's itertools.accumulate
- reduce_left: fold an iterable left with a function
- fold_left: fold an iterable left with a function and initial value
- mb_fold_left: fold an iterable left with a function and optional initial value

Shortcut versions of reduce - useful with infinite iterables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- sc_reduce_left: short circuit version of a left reduce
- sc_reduce_right: short circuit version of a right reduce

Installation:
-------------

| $ pip install pythonic-fp.iterables

Contribute:
-----------

- Project on PyPI: https://pypi.org/project/pythonic-fp.iterables
- Source Code: https://github.com/grscheller/pythonic-fp-iterables
- Issue Tracker: https://github.com/grscheller/pythonic-fp-iterables/issues
- Pull Requests: https://github.com/grscheller/pythonic-fp-iterables/pulls
- CHANGELOG: https://github.com/grscheller/pythonic-fp-iterables/blob/main/CHANGELOG.rst

+------------------------------------------------+----------------------+--------------------+
| Contributors                                   | Name                 | Role               |
+================================================+======================+====================+
| `@grscheller <https://github.com/grscheller>`_ | Geoffrey R. Scheller | author, maintainer |
+------------------------------------------------+----------------------+--------------------+

License Information
^^^^^^^^^^^^^^^^^^^

This project is licensed under the Apache License Version 2.0, January 2004.

See the `LICENCE file <https://github.com/grscheller/pythonic-fp-iterables/blob/main/LICENSE>`_
for details.
