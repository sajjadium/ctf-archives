from __future__ import annotations

from typing import Generic, TypeVar

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


class BijectionError(Exception, Generic[_VT]):
    """Must set a unique value in a BijectiveMap."""

    def __init__(self, value: _VT) -> None:
        self.value = value
        msg = 'The value "{}" is already in the mapping.'
        super().__init__(msg.format(value))


class BijectiveMap(dict[_KT, _VT]):
    """Invertible map."""

    inverse: BijectiveMap[_VT, _KT]

    def __init__(self, inverse: BijectiveMap[_VT, _KT] | None = None) -> None:
        if inverse is None:
            inverse = self.__class__(inverse=self)
        self.inverse = inverse

    def __setitem__(self, key: _KT, value: _VT) -> None:
        if value in self.inverse:
            raise BijectionError(value)

        self.inverse._set_item(value, key)
        self._set_item(key, value)

    def __delitem__(self, key: _KT) -> None:
        self.inverse._del_item(self[key])
        self._del_item(key)

    def _del_item(self, key: _KT) -> None:
        super().__delitem__(key)

    def _set_item(self, key: _KT, value: _VT) -> None:
        super().__setitem__(key, value)
