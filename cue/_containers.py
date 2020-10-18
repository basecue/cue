from __future__ import annotations

from ._base import publisher


class CueDict(dict):
    __setitem__ = publisher(dict.__setitem__)


class CueSet(set):
    add = publisher(set.add)
    remove = publisher(set.remove)
    discard = publisher(set.discard)
    clear = publisher(set.clear)


class CueList(list):
    append = publisher(list.append)
    remove = publisher(list.remove)
    clear = publisher(list.clear)
