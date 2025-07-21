# Copyright 2023-2025 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Module pythonic_fp.iterables.drop_take"""

from __future__ import annotations

__author__ = 'Geoffrey R. Scheller'
__copyright__ = 'Copyright (c) 2023-2025 Geoffrey R. Scheller'
__license__ = 'Apache License 2.0'

from collections.abc import Callable, Iterable, Iterator
from pythonic_fp.containers.box import Box
from .merging import concat

__all__ = [
    'drop',
    'drop_while',
    'take',
    'take_while',
    'take_split',
    'take_while_split',
]


## dropping and taking


def drop[D](iterable: Iterable[D], n: int) -> Iterator[D]:
    """Drop the next n values from iterable.

    .. code:: python

        def drop[D](
            iterable: Iterable[D],
            n: int
        ) -> Iterator[D]

    :param iterable: iterable whose values are to be dropped
    :param n: number of values to be dropped
    :return: an iterator of the remaining values

    """
    it = iter(iterable)
    for _ in range(n):
        try:
            next(it)
        except StopIteration:
            break
    return it


def drop_while[D](
        iterable: Iterable[D],
        pred: Callable[[D], bool]
    ) -> Iterator[D]:
    """Drop initial values from iterable while predicate is true.

    .. code:: python

        def drop_while[D](
            iterable: Iterable[D],
            pred: Callable[[D], bool]
        ) -> Iterator[D]

    :param iterable: iterable whose values are to be dropped
    :param pred: Boolean valued function
    :return: an iterator beginning where pred returned false

    """
    it = iter(iterable)
    while True:
        try:
            value = next(it)
            if not pred(value):
                it = concat((value,), it)
                break
        except StopIteration:
            break
    return it


def take[D](iterable: Iterable[D], n: int) -> Iterator[D]:
    """Return an iterator of up to n initial values of an iterable.

    .. code:: python

        def take[D](
            iterable: Iterable[D],
            n: int
        ) -> Iterator[D]

    :param iterable: iterable providing the values to be taken
    :param n: number of values to be dropped
    :return: an iterator of up to n initial values from iterable

    """
    it = iter(iterable)
    for _ in range(n):
        try:
            value = next(it)
            yield value
        except StopIteration:
            break


def take_while[D](
        iterable: Iterable[D],
        pred: Callable[[D], bool]
    ) -> Iterator[D]:
    """Yield values from iterable while predicate is true.

    .. code:: python

        def take_while[D](
            iterable: Iterable[D],
            pred: Callable[[D], bool]
        ) -> Iterator[D]

    .. warning::
        Risk of value loss if iterable is multiple referenced iterator.

    :param iterable: iterable providing the values to be taken
    :param pred: Boolean valued function
    :return: an Iterator of up to n initial values from the iterable

    """
    it = iter(iterable)
    while True:
        try:
            value = next(it)
            if pred(value):
                yield value
            else:
                break
        except StopIteration:
            break


def take_split[D](
        iterable: Iterable[D],
        n: int
    ) -> tuple[Iterator[D], Iterator[D]]:
    """Same as take except also return iterator of remaining values.

    .. code:: python

        def take_split[D](
            iterable: Iterable[D],
            n: int
        ) -> tuple[Iterator[D], Iterator[D]]

    .. Warning::

       **CONTRACT:** Do not access the second returned iterator until the
       first one is exhausted.

    :param iterable: iterable providing the values to be taken
    :param n: maximum number of values to be taken
    :return: an iterator of values taken and an iterator of remaining values

    """
    it = iter(iterable)
    itn = take(it, n)

    return itn, it


def take_while_split[D](
    iterable: Iterable[D], pred: Callable[[D], bool]
) -> tuple[Iterator[D], Iterator[D]]:
    """Yield values from iterable while predicate is true.

    .. code:: python

        def take_while_split[D](
            iterable: Iterable[D],
            pred: Callable[[D], bool]
        ) -> tuple[Iterator[D], Iterator[D]]

    .. Warning::

       **CONTRACT:** Do not access the second returned iterator until
       the first one is exhausted.

    :param iterable: iterable providing the values to be taken
    :param pred: Boolean valued function
    :return: an iterator of values taken and an iterator of remaining values

    """
    def _take_while(
        it: Iterator[D], pred: Callable[[D], bool], val: Box[D]
    ) -> Iterator[D]:
        while True:
            try:
                val.put(next(it))
                if pred(val.get()):
                    yield val.pop()
                else:
                    break
            except StopIteration:
                break

    it = iter(iterable)
    value: Box[D] = Box()
    it_pred = _take_while(it, pred, value)

    return (it_pred, concat(value, it))
