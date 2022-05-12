from functools import wraps

from .._compat.typing import Any, Callable, ContextManager, Optional, TypeVar


_Self = TypeVar('_Self')
_R = TypeVar('_R')
_WrappedType = Callable[..., _R]


def define_guard(
    guard_fn: Callable[[_Self], Optional[ContextManager]]
)-> Callable[[_WrappedType], _WrappedType]:
    def decorator(wrapped: _WrappedType) -> _WrappedType:
        @wraps(wrapped)
        def wrapper_guards(self: _Self, *args: Any, **kwargs: Any) -> _R:
            ret_val = guard_fn(self)
            if ret_val is not None:
                with ret_val:
                    return wrapped(self, *args, **kwargs)
            else:
                return wrapped(self, *args, **kwargs)

        return wrapper_guards

    return decorator
