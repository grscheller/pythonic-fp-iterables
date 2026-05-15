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
.. admonition:: Merging iterables

    Functions to merge multiple iterables together into one.

"""

from collections.abc import Iterable, Iterator
from enum import auto, Enum

__all__ = [
    'MergeEnum',
    'concat',
    'merge',
    'exhaust',
    'blend',
]


class MergeEnum(Enum):
    """
    .. admonition:: Iterable Blending Enums.

        - **Concat:** Concatenate first to last
        - **Merge:** Merge until one is exhausted
        - **Exhaust:** Merge until all are exhausted

    """
    Concat = auto()
    Merge = auto()
    Exhaust = auto()


def concat[D](*iterables: Iterable[D]) -> Iterator[D]:
    """
    .. admonition:: concatenate iterables

        Sequentially concatenate multiple iterables.

        :param iterables: Iterables to concatenate.
        :yields: The concatenated items from all the iterables.

        .. warning::
            An infinite iterable will prevent subsequent iterables from
            yielding any items.

        .. note::

            Performant to the standard library's ``itertools.chain``.

    """
    for iterator in map(lambda x: iter(x), iterables):
        while True:
            try:
                item = next(iterator)
                yield item
            except StopIteration:
                break


def merge[D](*iterables: Iterable[D], yield_partials: bool = False) -> Iterator[D]:
    """
    .. admonition:: merge iterables

        Merge multiple iterables until one of them is exhausted.

        :param iterables: Iterables to merge until one gets exhausted.
        :param yield_partials: Yield any unpaired yielded items from other iterables.
        :yields: Merged items from the iterables until one of the
                 iterables is exhausted.

        .. note::

            When ``yield_partials`` is true, then any unmatched items
            from other iterables already yielded when the first iterable
            is exhausted are yielded.

            This prevents data lose if any of the iterables are
            iterators with external references.

    """
    iter_list = list(map(lambda x: iter(x), iterables))
    items = []
    if (num_iters := len(iter_list)) > 0:
        while True:
            try:
                for ii in range(num_iters):
                    items.append(next(iter_list[ii]))
                yield from items
                items.clear()
            except StopIteration:
                break
        if yield_partials:
            yield from items


def exhaust[D](*iterables: Iterable[D]) -> Iterator[D]:
    """
    .. admonition:: exhaustively merge iterables

        Merge multiple iterables until all of them are exhausted.

        :param iterables: Iterables to exhaustively merge.
        :yields: Merged items from the iterables until all of the
                 iterables are exhausted.

    """
    iter_list = list(map(lambda x: iter(x), iterables))
    if (num_iters := len(iter_list)) > 0:
        ii = 0
        items = []
        while True:
            try:
                while ii < num_iters:
                    items.append(next(iter_list[ii]))
                    ii += 1
                yield from items
                ii = 0
                items.clear()
            except StopIteration:
                num_iters -= 1
                if num_iters < 1:
                    break
                del iter_list[ii]

        yield from items


def blend[D](
    *iterables: Iterable[D],
    merge_enum: MergeEnum = MergeEnum.Concat,
    yield_partials: bool = False,
) -> Iterator[D]:
    """
    .. admonition:: merge iterables

        Merge behavior based on value of merge_enum parameter.

        - Concat: Concatenate first to last
        - Merge: Merge until one is exhausted
        - Exhaust: Merge until all are exhausted

        :param iterables: Iterables to blend together.
        :param merge_enum: ``MergeEnum`` to determine merging behavior.
        :param yield_partials: Yield unpaired items from other iterables.
        :yields: Items from all iterables blended together.
        :raises ValueError: When an unknown ``MergeEnum`` is given.

    """
    match merge_enum:
        case MergeEnum.Concat:
            return concat(*iterables)
        case MergeEnum.Merge:
            return merge(*iterables, yield_partials=yield_partials)
        case MergeEnum.Exhaust:
            return exhaust(*iterables)

    raise ValueError('Unknown MergeEnum given')
