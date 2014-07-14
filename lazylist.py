#!/usr/bin/env python3

import collections.abc
from itertools import islice

__all__ = ['LazyList']

class LazyList(collections.abc.MutableSequence):
    def __init__(self, iterable):
        self._nonlazy, self._lazy = [], iter(iterable)
    def __len__(self):
        self._delazify()
        return len(self._nonlazy)
    def _delazify(self, index=None):
        if index is None:
            self._nonlazy.extend(self._lazy)
            return
        if isinstance(index, slice):
            if index.start < 0 or index.stop < 0:
                self._delazify()
                return
            index = range(index.start, index.stop, index.step)[-1]
        if index < 0:
            self._delazify()
            return
        self._nonlazy.extend(islice(self._lazy, index - len(self._nonlazy) + 1))
    def __getitem__(self, index):
        self._delazify(index)
        return self._nonlazy[index]
    def __delitem__(self, index):
        self._delazify(index)
        del self._nonlazy[index]
    def __setitem__(self, index, value):
        self._delazify(index)
        self._nonlazy[index] = value
    def insert(self, index, value):
        if index:
            self._delazify(index-1)
        self._nonlazy.insert(index, value)
    def __iter__(self):
        yield from self._nonlazy
        for value in self._lazy:
            self._nonlazy.append(value)
            yield value
    def append(self, value):
        self._lazy = chain(self._lazy, (value,))
    def extend(self, values):
        self._lazy = chain(self._lazy, values)
    def clear(self):
        self._nonlazy, self._lazy = [], iter(())
    def __str__(self):
        return '[{}]'.format(', '.join(list(map(repr, self._nonlazy)) + ['...']))
    def __repr__(self):
        return 'LazyList({})'.format(self)

if __name__ == '__main__':
    import sys
    ll = LazyList(sys.argv)
    print(ll)
    print(ll[1])
    print(ll)
    print(ll[-3:-2])
    print(ll)

