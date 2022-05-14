import sublime

from uuid import uuid4
from functools import partial
from collections.abc import Mapping

from ._util.collections import get_selector
from ._util.named_value import NamedValue

from ._compat.typing import Any, Callable, Iterable, NoReturn, TypeVar, Union, Mapping as _Mapping

_Default = TypeVar('_Default')
Value = Union[bool, int, float, str, list, dict, None]

__all__ = ['SettingsDict', 'NamedSettingsDict']


_NO_DEFAULT = NamedValue('SettingsDict.NO_DEFAULT')


class SettingsDict():
    """Wraps a :class:`sublime.Settings` object `settings`
    with a :class:`dict`-like interface.

    There is no way to list or iterate over the keys of a
    :class:`~sublime.Settings` object. As a result, the following methods are
    not implemented:

    - :meth:`__len__`
    - :meth:`__iter__`
    - :meth:`clear`
    - :meth:`copy`
    - :meth:`items`
    - :meth:`keys`
    - :meth:`popitem`
    - :meth:`values`

    You can use :class:`collections.ChainMap` to chain a :class:`SettingsDict`
    with other dict-like objects. If you do, calling the above unimplemented
    methods on the :class:`~collections.ChainMap` will raise an error.
    """

    NO_DEFAULT = _NO_DEFAULT

    def __init__(self, settings: sublime.Settings):
        self.settings = settings

    def __iter__(self) -> NoReturn:
        """Raise NotImplementedError."""
        raise NotImplementedError()

    def __getitem__(self, key: str) -> Value:
        """Return the setting named `key`.

        If a subclass of :class:`SettingsDict` defines a method :meth:`__missing__`
        and `key` is not present,
        the `d[key]` operation calls that method with `key` as the argument.
        The `d[key]` operation then returns or raises
        whatever is returned or raised by the ``__missing__(key)`` call.
        No other operations or methods invoke :meth:`__missing__`.
        If :meth:`__missing__` is not defined, :exc:`KeyError` is raised.
        :meth:`__missing__` must be a method; it cannot be an instance variable.

        :raise KeyError: if there is no setting with the given `key`
            and :meth:`__missing__` is not defined.
        """
        if key in self:
            return self.get(key)
        else:
            return self.__missing__(key)

    def __missing__(self, key: str) -> Value:
        raise KeyError(key)

    def __setitem__(self, key: str, value: Value) -> None:
        """Set `self[key]` to `value`."""
        self.settings.set(key, value)

    def __delitem__(self, key: str) -> None:
        """Remove `self[key]` from `self`.

        :raise KeyError: if there us no setting with the given `key`.
        """
        if key in self:
            self.settings.erase(key)
        else:
            raise KeyError(key)

    def __contains__(self, item: str) -> bool:
        """Return ``True`` if `self` has a setting named `key`, else ``False``."""
        return self.settings.has(item)

    def get(self, key: str, default: _Default = None) -> Union[Value, _Default]:
        """Return the value for `key` if `key` is in the dictionary, or `default` otherwise.

        If `default` is not given, it defaults to ``None``,
        so that this method never raises :exc:`KeyError`."""
        return self.settings.get(key, default)

    def pop(
        self, key: str, default: Union[_Default, NamedValue] = _NO_DEFAULT
    ) -> Union[Value, _Default]:
        """Remove the setting `self[key]` and return its value or `default`.

        :raise KeyError: if `key` is not in the dictionary
            and `default` is :attr:`SettingsDict.NO_DEFAULT`.

        .. versionchanged:: 1.2
            Added :attr:`SettingsDict.NO_DEFAULT`.
        """
        if key in self:
            ret = self[key]
            del self[key]
            return ret
        elif default is _NO_DEFAULT:
            raise KeyError(key)
        else:
            return default  # type: ignore

    def setdefault(self, key: str, default: Value = None) -> Value:
        """Set `self[key]` to `default` if it wasn't already defined and return `self[key]`.
        """
        if key in self:
            return self[key]
        else:
            self[key] = default
            return default

    def update(
        self,
        other: Union[_Mapping[str, Value], Iterable[Iterable[str]]] = [],
        **kwargs: Value
    ) -> None:
        """Update the dictionary with the key/value pairs from `other`,
        overwriting existing keys.

        Accepts either another dictionary object
        or an iterable of key/value pairs (as tuples or other iterables of length two).
        If keyword arguments are specified,
        the dictionary is then updated with those key/value pairs:
        ``self.update(red=1, blue=2)``.
        """
        if isinstance(other, Mapping):
            other = other.items()  # type: ignore

        for key, value in other:
            self[key] = value

        for key, value in kwargs.items():
            self[key] = value

    def subscribe(
        self, selector: Any, callback: Callable, default_value: Any = None
    ) -> Callable[[], None]:
        """Register a callback to be invoked
        when the value derived from the settings object changes
        and return a function that when invoked will unregister the callback.

        Instead of passing the `SettingsDict` to callback,
        a value derived using `selector` is passed.
        If `selector` is callable, then ``selector(self)`` is passed.
        If `selector` is a :class:`str`,
        then ``self.get(selector, default_value)`` is passed.
        Otherwise, ``projection(self, selector)`` is passed.

        `callback` should accept two arguments:
        the new derived value and the previous derived value.

        ..  versionchanged:: 1.1
            Return an unsubscribe callback.
        """
        selector_fn = get_selector(selector)

        previous_value = selector_fn(self)

        def onchange() -> None:
            nonlocal previous_value
            new_value = selector_fn(self)

            if new_value != previous_value:
                callback(new_value, previous_value)
                previous_value = new_value

        key = str(uuid4())
        self.settings.add_on_change(key, onchange)
        return partial(self.settings.clear_on_change, key)


class NamedSettingsDict(SettingsDict):
    """Wraps a :class:`sublime.Settings` object corresponding to a `sublime-settings` file."""

    @property
    def file_name(self) -> str:
        """The name of the sublime-settings files
        associated with the :class:`NamedSettingsDict`."""
        return self.name + '.sublime-settings'

    def __init__(self, name: str):
        """Return a new :class:`NamedSettingsDict` corresponding to the given name."""

        if name.endswith('.sublime-settings'):
            self.name = name[:-17]
        else:
            self.name = name

        super().__init__(sublime.load_settings(self.file_name))

    def save(self) -> None:
        """Flush any in-memory changes to the :class:`NamedSettingsDict` to disk."""
        sublime.save_settings(self.file_name)
