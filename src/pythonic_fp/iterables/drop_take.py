# Copyright 2023-2026 Geoffrey R. Scheller
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

"""
.. admonition:: Drop and Take

    Functions which drop or take items from an iterable.

    .. important::

        If iterable is a multiply referenced iterator, items
        dropped or taken need not be the next consecutive items.

    .. important::

        If iterable is mutable, iterator may be affected by the
        current state of the original iterable.

        .. tip::

            Prefer immutable iterables over mutable ones.

"""

from collections.abc import Callable, Iterable, Iterator
from pythonic_fp.gadgets.box import Box
from .merging import concat

__all__ = [
    'drop',
    'drop_while',
    'take',
    'take_while',
    'take_split',
    'take_while_split',
]


def drop[D](iterable: Iterable[D], n: int) -> Iterator[D]:
    """
    .. admonition:: drop

        Drop the next n items from iterable.

        :param iterable: Iterable whose items are to be dropped.
        :param n: Number of items to be dropped.
        :yields: The remaining items.

    """
    iterator = iter(iterable)
    for _ in range(n):
        try:
            next(iterator)
        except StopIteration:
            break
    return iterator


def drop_while[D](iterable: Iterable[D], pred: Callable[[D], bool]) -> Iterator[D]:
    """
    .. admonition:: drop while

        Drop initial items from iterable while predicate is true.

        :param iterable: Iterable whose items are to be dropped.
        :param pred: Single argument Boolean valued function.
        :yields: items starting when ``pred`` returns ``False``.

    """
    iterator = iter(iterable)
    while True:
        try:
            item = next(iterator)
            if not pred(item):
                iterator = concat((item,), iterator)
                break
        except StopIteration:
            break
    return iterator


def take[D](iterable: Iterable[D], n: int) -> Iterator[D]:
    """
    .. admonition:: take

        Return an iterator yielding up to n items from an iterable.

        :param Iterable: Iterable providing the items to be taken.
        :param n: Number of items to be taken.
        :yields: Up to n items from iterable.

    """
    iterator = iter(iterable)
    for _ in range(n):
        try:
            item = next(iterator)
            yield item
        except StopIteration:
            break


def take_while[D](iterable: Iterable[D], pred: Callable[[D], bool]) -> Iterator[D]:
    """
    .. admonition:: take while

        Return an iterator of items until predicate false.

        :param iterable: Iterable providing the items to be taken.
        :param pred: Single argument Boolean valued function.
        :yields: Items from iterable while predicate is true.

        .. warning::

            Risk of data loss if iterable is multiple referenced iterator.

    """
    iterator = iter(iterable)
    while True:
        try:
            item = next(iterator)
            if pred(item):
                yield item
            else:
                break
        except StopIteration:
            break


def take_split[D](iterable: Iterable[D], n: int) -> tuple[Iterator[D], Iterator[D]]:
    """
    .. admonition:: take split

        Same as take except also return an iterator of
        the remaining items.

        .. admonition:: CONTRACT

            **IMPORTANT:** Do not access the second iterator until
            the first one is completely exhausted.

        :param iterable: Iterable providing the items to be taken.
        :param n: maximum Number of items to be taken.
        :returns: A tuple containing an iterator of items taken
                  and an iterator of remaining items.

    """
    iterator = iter(iterable)
    itn = take(iterator, n)

    return itn, iterator


def take_while_split[D](
    iterable: Iterable[D], pred: Callable[[D], bool]
) -> tuple[Iterator[D], Iterator[D]]:
    """
    .. admonition:: take while

        Same as take_while except also return an iterator of
        the remaining items.

        .. admonition:: CONTRACT

            **IMPORTANT:** Do not access the second iterator until
            the first one is completely exhausted.

        :param iterable: Iterable providing the items to be taken.
        :param pred: Single argument Boolean valued function.
        :returns: A tuple containing an iterator of items taken while
                  ``pred`` truthy and an iterator of remaining items.

    """

    def _take_while(
        iterator: Iterator[D], pred: Callable[[D], bool], val: Box[D]
    ) -> Iterator[D]:
        while True:
            try:
                val.put(next(iterator))
                if pred(val.get()):
                    yield val.pop()
                else:
                    break
            except StopIteration:
                break

    iterator = iter(iterable)
    item: Box[D] = Box()
    it_pred = _take_while(iterator, pred, item)

    return it_pred, concat(item, iterator)
