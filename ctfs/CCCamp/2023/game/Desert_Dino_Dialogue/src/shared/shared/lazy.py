import builtins
from collections.abc import Iterator
from enum import EnumMeta
from typing import Any

import betterproto


class Lazy:
    cls: type

    def __init__(self, cls: type) -> None:
        self.cls = cls

    def get_default(self, sub_cls: type) -> Any:
        match sub_cls:
            case builtins.str:
                return ""
            case builtins.int:
                return 0
            case builtins.float:
                return 0.0
            case builtins.bool:
                return False
            case builtins.bytes:
                return b""
            case builtins.list:
                return LazyList([], cls=sub_cls)
            case EnumMeta():
                return list(sub_cls)[0]
            case _:
                return LazyDict({}, cls=sub_cls)


class LazyList(list[Any], Lazy):
    def __init__(self, a: list[Any], cls: type) -> None:
        Lazy.__init__(self=self, cls=cls)
        super().__init__(a)

    def __getitem__(self, items: Any) -> Any:
        ret = super().__getitem__(items)

        match ret:
            case dict():
                new_value = LazyDict(ret, cls=self.cls)
            case list():
                new_value = LazyList(ret, cls=self.cls)
            case _:
                new_value = ret

        super().__setitem__(items, new_value)
        return new_value

    def __iter__(self) -> Iterator[Any]:
        for ret in super().__iter__():
            match ret:
                case dict():
                    yield LazyDict(ret, cls=self.cls)
                case list():
                    yield LazyList(ret, cls=self.cls)
                case _:
                    yield ret


class LazyDict(dict[str, Any], Lazy):
    def __init__(self, a: dict[str, Any], cls: type) -> None:
        Lazy.__init__(self=self, cls=cls)
        super().__init__(a)
        self.object = None

    def __getattr__(self, __name: str) -> Any:
        if self.object:
            return self.object.__getattribute__(__name)

        key = betterproto.casing.camel_case(__name)

        sub_cls: Any = self.cls._cls_for(self.cls.__dataclass_fields__[__name])  # type: ignore

        if key in self:
            ret = self[key]

            match sub_cls:
                case EnumMeta():
                    new_value = sub_cls(ret)
                case _:
                    match ret:
                        case dict():
                            new_value = LazyDict(ret, cls=sub_cls)
                        case list():
                            new_value = LazyList(ret, cls=sub_cls)
                        case _:
                            new_value = ret

        else:
            new_value = self.get_default(sub_cls)

        self[key] = new_value
        return new_value

    @property  # type: ignore
    def __class__(self) -> type:
        return self.cls

    def to_dict(
        self,
        casing: betterproto.Casing = betterproto.Casing.CAMEL,
        include_default_values: bool = False,
    ) -> dict[str, Any]:
        if not self.object:
            value = self.cls().from_dict(self)

            self.object = value

        return self.object.to_dict(casing, include_default_values)
