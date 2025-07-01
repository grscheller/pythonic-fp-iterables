# Pythonic FP - Tools for iterables

Tools to create iterators from iterables, part of the PyPI
[pythonic-fp](https://github.com/grscheller/pythonic-fp/blob/main/README.rst)
Namespace Projects.

Detailed API
[documentation](https://grscheller.github.io/pythonic-fp/maintained/iterables)
on *GH-Pages*.

## Features:

- Concatenating and merging iterables
- Dropping and taking values from iterables
- Reducing and accumulating iterables
- Assumptions
  - iterables are not necessarily iterators
  - at all times iterator protocol is assumed to be followed
    - all iterators are assumed to be iterable
    - for all iterators `my_iter` we assume `iter(my_iter) is my_iter`

### Functions to merge iterables

- concat: concatenate multiple iterables sequentially
- exhaust: shuffle together multiple iterables until all are exhausted
- merge: shuffle together multiple iterables until one is exhausted

### Dropping and taking

| function | return iterator yielding values from ds |
|:-------- |:--------------------------------------- |
| drop(ds, n) | with first n values of ds dropped |
| drop_while(ds, pred) | dropping values until predicate false |
| take(ds, n) | yielding first n values of ds |
| take_while(ds, pred) | yielding values from ds while predicate true |

| function | return a pair of iterators |
|:-------- |:-------------------------- |
take_split(ds, n) | like take but second iterator yields remaining values |
take_while_split(ds, pred) | like take_while, second iterator yields remaining values |

### Functions to accumulate and reduce

| function | description |
|:-------- |:----------- |
| accumulate | pure Python version of std library's itertools.accumulate |
| reduce_left | fold an iterable left with a function |
| fold_left | fold an iterable left with a function and initial value |
| mb_fold_left | fold an iterable left with a function and optional initial value |

### Shortcut versions of reduce - useful with infinite iterables

| function | description |
|:-------- |:----------- |
| sc_reduce_left | short circuit version of a left reduce |
| sc_reduce_right | short circuit version of a right reduce |

This PyPI project is part of of the grscheller
[pythonic-fp namespace projects](https://grscheller.github.io/pythonic-fp/).

## Documentation

Documentation hosted on
[GitHub Pages](https://grscheller.github.io/pythonic-fp-iterables/).

## Copyright and License

Copyright (c) 2023-2025 Geoffrey R. Scheller. Licensed under the Apache
License, Version 2.0. See the LICENSE file for details.
