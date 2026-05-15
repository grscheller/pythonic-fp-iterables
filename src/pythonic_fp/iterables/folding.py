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
.. admonition:: Folding and Accumulating

    Functions to reduce and accumulate items from iterables.

"""

from collections.abc import Callable, Iterable, Iterator
from typing import cast, Never
from pythonic_fp.fptools.function import negate, swap
from pythonic_fp.fptools.maybe import MayBe
from pythonic_fp.gadgets.sentinels.novalue import NoValue
from .drop_take import drop_while, take_while_split

__all__ = [
    'accumulate',
    'reduce_left',
    'fold_left',
    'maybe_fold_left',
    'sc_reduce_left',
    'sc_reduce_right',
]


def accumulate[D, L](
    iterable: Iterable[D], f: Callable[[L, D], L], initial: L | NoValue = NoValue()
) -> Iterator[L]:
    """
    .. admonition:: accumulate

        Returns an iterator of partial fold items. A pure Python
        version of 

        :param iterable: Iterable to be folded.
        :param f: Two parameter function, first parameter for accumulated items.
        :param initial: Optional ``initial`` item to start fold.
        :yields: The intermediate folded items.

        .. note::

            A pure Python implementation of the standard
            library's ``itertools.accumulate``

            - function ``f`` does not default to addition (for typing flexibility)
            - begins accumulation with an optional ``initial`` item

    """
    it = iter(iterable)
    try:
        it0 = next(it)
    except StopIteration:
        if initial is NoValue():
            return
        yield cast(L, initial)
    else:
        if initial is not NoValue():
            init = cast(L, initial)
            yield init
            acc = f(init, it0)
            for ii in it:
                yield acc
                acc = f(acc, ii)
            yield acc
        else:
            acc = cast(L, it0)  # in this case L = D
            for ii in it:
                yield acc
                acc = f(acc, ii)
            yield acc


def reduce_left[D](iterable: Iterable[D], f: Callable[[D, D], D]) -> D | Never:
    """
    .. admonition:: reduce left

        Fold an iterable left with a function.

        :param iterable: Iterable to be reduced (folded).
        :param f: Two parameter function, first parameter for accumulated items.
        :return: Reduced item from the iterable.
        :raises StopIteration: When called on an empty iterable.
        :raises Exception: Does not catch any exceptions from ``f``.

        .. warning::

            - never returns if given an infinite iterable
            - does not catch or re-raises exceptions raised by ``f``

    """
    it = iter(iterable)
    try:
        acc = next(it)
    except StopIteration as exc:
        msg = 'Attempt to reduce an empty iterable?'
        raise StopIteration(msg) from exc

    for v in it:
        acc = f(acc, v)

    return acc


def fold_left[D, L](
    iterable: Iterable[D], f: Callable[[L, D], L], initial: L
) -> L | Never:
    """
    .. admonition:: fold left

        Fold an iterable left with a function and initial item.

        - not restricted to ``__add__`` for the folding function
        - initial item is required, does not default to ``0``
        - handles non-numeric data just find

        :param iterable: iterable to be folded
        :param f: two parameter function, first parameter for accumulated item
        :param initial: mandatory initial item to start fold
        :return: the folded item

        .. warning::

            - never returns if given an infinite iterable
            - does not catch or re-raises exceptions raised by ``f``

    """
    acc = initial
    for v in iterable:
        acc = f(acc, v)
    return acc


def maybe_fold_left[D, L](
    iterable: Iterable[D], f: Callable[[L, D], L], initial: L | NoValue = NoValue()
) -> MayBe[L] | Never:
    """
    .. admonition:: maybe fold left

        Folds an iterable left with an "optional" initial item.

        - when an initial item is not given then ``L = D``
        - if iterable empty and no ``initial`` item given, return ``MayBe()``

        :param iterable: The iterable to be folded.
        :param f: First argument is for the accumulated items.
        :param initial: Mandatory initial item to start fold.
        :return: ``MayBe`` of a successfully folded item,
                 otherwise returns ``MayBe()``.

        .. warning::

            - never returns if given an infinite iterable
            - any exception ``f`` raises is thrown away

    """
    acc: L
    it = iter(iterable)
    if initial is NoValue():
        try:
            acc = cast(L, next(it))  # in this case L = D
        except StopIteration:
            return MayBe()
    else:
        acc = cast(L, initial)

    for v in it:
        try:
            acc = f(acc, v)
        except Exception:
            return MayBe()

    return MayBe(acc)


def sc_reduce_left[D](
    iterable: Iterable[D],
    f: Callable[[D, D], D],
    start: Callable[[D], bool] = (lambda d: True),
    stop: Callable[[D], bool] = (lambda d: False),
    include_start: bool = True,
    include_stop: bool = True,
) -> tuple[MayBe[D], Iterator[D]]:
    """
    .. admonition:: short circuit reduce left

        Short circuit version of a left fold.

        :param iterable: Iterable to be reduced from the left.
        :param f: Two parameter function, first parameter for
                  the accumulator.
        :param start: Delay starting the fold until it returns true.
        :param stop: Prematurely stop the fold when it returns true.
        :param include_start: If true, include starting item in fold.
        :param include_stop: If true, include stopping item in fold.
        :return: Tuple of a ``MayBe`` of the folded item and iterator
                 of remaining iterables.

        .. note::

            Behavior for default arguments will

            - left reduce finite iterable
            - start folding immediately
            - continue folding until end (of a possibly infinite iterable)

            .. tip::

                Useful for infinite iterables when Callable ``stop``
                is provided.

    """
    it_start = drop_while(iterable, negate(start))
    if not include_start:
        try:
            next(it_start)
        except StopIteration:
            pass
    it_reduce, it_rest = take_while_split(it_start, negate(stop))
    mb_reduced = maybe_fold_left(it_reduce, f)
    if include_stop:
        if mb_reduced:
            try:
                last = next(it_rest)
                mb_reduced = MayBe(f(mb_reduced.get(), last))
            except StopIteration:
                pass
        else:
            try:
                last = next(it_rest)
                mb_reduced = MayBe(last)
            except StopIteration:
                pass

    return (mb_reduced, it_rest)


def sc_reduce_right[D](
    iterable: Iterable[D],
    f: Callable[[D, D], D],
    start: Callable[[D], bool] = (lambda d: False),
    stop: Callable[[D], bool] = (lambda d: False),
    include_start: bool = True,
    include_stop: bool = True,
) -> tuple[MayBe[D], Iterator[D]]:
    """
    .. admonition:: short circuit reduce right

        Short circuit version of a right fold.

        :param iterable: Iterable to be reduced from the right.
        :param f: Two parameter function, second parameter for
                  the accumulator.
        :param start: Delay starting the fold until it returns true.
        :param stop: Prematurely stop the fold when it returns true.
        :param include_start: If true, include starting item.
        :param include_stop: If true, include stopping item in fold.
        :return: Tuple of a ``MayBe`` of the folded item and iterator
                 of remaining iterables.

        .. note::

            Behavior for default arguments will

            - right reduce finite iterable
            - start folding at end (of a possibly infinite iterable)
            - continue reducing right until beginning

            .. tip::

                Useful for infinite and non-reversible iterables.

    """
    it_start, it_rest = take_while_split(iterable, negate(start))
    list1 = list(it_start)
    if include_start:
        try:
            begin = next(it_rest)
        except StopIteration:
            pass
        else:
            list1.append(begin)

    list1.reverse()
    it_reduce, it_stop = take_while_split(list1, negate(stop))

    mb_reduced = maybe_fold_left(it_reduce, swap(f))
    if include_stop:
        try:
            end = next(it_stop)
        except StopIteration:
            pass
        else:
            if mb_reduced:
                mb_reduced = MayBe(f(end, mb_reduced.get()))
            else:
                mb_reduced = MayBe(end)

    return (mb_reduced, it_rest)
