Usage
=====

How to install the package
--------------------------

Install the project into your Python environment:

.. code:: console

    $ pip install pythonic-fp.iterables

Importing the package
---------------------

Import the functions and the enum into your code.

.. code:: python

    from pythonic_fp.iterables.merging import concat, merge, exhaust
    from pythonic_fp.iterables.merging import MergeEnum, blend

    from pythonic_fp.iterables.drop_take import drop, drop_while
    from pythonic_fp.iterables.drop_take import take, take_while
    from pythonic_fp.iterables.drop_take import take_split, take_while_split

    from pythonic_fp.iterables.folding import accumulate
    from pythonic_fp.iterables.folding import reduce_left
    from pythonic_fp.iterables.folding import fold_left, maybe_fold_left
    from pythonic_fp.iterables.folding import sc_reduce_left, sc_reduce_right
