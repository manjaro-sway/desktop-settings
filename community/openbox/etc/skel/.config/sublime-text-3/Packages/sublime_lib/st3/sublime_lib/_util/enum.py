from functools import partial
from ..vendor.python.enum import EnumMeta, Enum, Flag

from .._compat.typing import Any, Callable, Optional


__all__ = ['ExtensibleConstructorMeta', 'construct_with_alternatives', 'construct_union']


class ExtensibleConstructorMeta(EnumMeta):
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        return cls.__new__(cls, *args, **kwargs)


def extend_constructor(
    constructor: Callable[..., Enum]
) -> Callable[[EnumMeta], EnumMeta]:
    def decorator(cls: EnumMeta) -> EnumMeta:
        next_constructor = partial(cls.__new__, cls)

        def __new__(cls: EnumMeta, *args: Any, **kwargs: Any) -> Enum:
            return constructor(next_constructor, cls, *args, **kwargs)

        cls.__new__ = __new__  # type: ignore
        return cls

    return decorator


def construct_with_alternatives(
    provider: Callable[..., Optional[Enum]]
) -> Callable[[EnumMeta], EnumMeta]:
    def constructor(next_constructor: Callable[..., Enum], cls: EnumMeta,
                    *args: Any, **kwargs: Any) -> Enum:
        try:
            return next_constructor(*args, **kwargs)
        except ValueError:
            result = provider(cls, *args, **kwargs)
            if result is None:
                raise
            else:
                return result

    return extend_constructor(constructor)


def _construct_union(
    next_constructor: Callable[[Any], Flag],
    cls: ExtensibleConstructorMeta,
    *args: Any
) -> Any:
    if args:
        ret, *rest = iter(next_constructor(arg) for arg in args)
        for value in rest:
            ret |= value

        return ret
    else:
        return next_constructor(0)


construct_union = extend_constructor(_construct_union)
