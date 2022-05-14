import sublime

import inspect

from .vendor.python.enum import Enum
from ._util.enum import ExtensibleConstructorMeta, construct_with_alternatives
from .syntax import get_syntax_for_scope
from .encodings import to_sublime

from ._compat.typing import Any, Optional, Mapping


__all__ = ['LineEnding', 'new_view', 'close_view']


def case_insensitive_value(cls: ExtensibleConstructorMeta, value: str) -> Optional[Enum]:
    return next((
        member for name, member in cls.__members__.items()
        if name.lower() == value.lower()
    ), None)


@construct_with_alternatives(case_insensitive_value)
class LineEnding(Enum, metaclass=ExtensibleConstructorMeta):
    """An :class:`Enum` of line endings supported by Sublime Text.

    The :class:`LineEnding` constructor accepts either
    the case-insensitive name (e.g. ``'unix'``) or the value (e.g. ``'\\n'``) of a line ending.

    .. py:attribute:: Unix
        :annotation: = '\\n'

    .. py:attribute:: Windows
        :annotation: = '\\r\\n'

    .. py:attribute:: CR
        :annotation: = '\\r'

    .. versionadded:: 1.2
    """
    Unix = '\n'
    Windows = '\r\n'
    CR = '\r'


def new_view(window: sublime.Window, **kwargs: Any) -> sublime.View:
    """Open a new view in the given `window`, returning the :class:`~sublime.View` object.

    This function takes many optional keyword arguments:

    :argument content: Text to be inserted into the new view. The text will be inserted even
        if the `read_only` option is ``True``.

    :argument encoding: The encoding that the view should use when saving.

    :argument line_endings: The kind of line endings to use.
        The given value will be passed to :class:`LineEnding`.

    :argument name: The name of the view. This will be shown as the title of the view's tab.

    :argument overwrite: If ``True``, the view will be in overwrite mode.

    :argument read_only: If ``True``, the view will be read-only.

    :argument scope: A scope name.
        The view will be assigned a syntax definition that corresponds to the given scope
        (as determined by :func:`~sublime_lib.get_syntax_for_scope`).
        Incompatible with the `syntax` option.

    :argument scratch: If ``True``, the view will be a scratch buffer.
        The user will not be prompted to save the view before closing it.

    :argument settings: A dictionary of names and values
        that will be applied to the new view's Settings object.

    :argument syntax: The resource path of a syntax definition that the view will use.
        Incompatible with the `scope` option.

    :raise ValueError: if both `scope` and `syntax` are specified.
    :raise ValueError: if `encoding` is not a Python encoding name.
    :raise ValueError: if `line_endings` cannot be converted to :class:`LineEnding`.

    ..  versionchanged:: 1.2
        Added the `line_endings` argument.
    """
    validate_view_options(kwargs)

    view = window.new_file()
    set_view_options(view, **kwargs)
    return view


def close_view(view: sublime.View, *, force: bool = False) -> None:
    """Close the given view, discarding unsaved changes if `force` is ``True``.

    If the view is invalid (e.g. already closed), do nothing.

    :raise ValueError: if the view has unsaved changes and `force` is not ``True``.
    :raise ValueError: if the view is not closed for any other reason.
    """
    if view.is_dirty() and not view.is_scratch():
        if force:
            view.set_scratch(True)
        else:
            raise ValueError('The view has unsaved changes.')

    if not view.close():
        raise ValueError('The view could not be closed.')


def validate_view_options(options: Mapping[str, Any]) -> None:
    unknown = set(options) - VIEW_OPTIONS
    if unknown:
        raise ValueError('Unknown view options: %s.' % ', '.join(list(unknown)))

    if 'scope' in options and 'syntax' in options:
        raise ValueError('The "syntax" and "scope" arguments are exclusive.')

    if 'line_endings' in options:
        LineEnding(options['line_endings'])


def set_view_options(
    view: sublime.View,
    *,
    name: Optional[str] = None,
    settings: Optional[dict] = None,
    read_only: Optional[bool] = None,
    scratch: Optional[bool] = None,
    overwrite: Optional[bool] = None,
    syntax: Optional[str] = None,
    scope: Optional[str] = None,
    encoding: Optional[str] = None,
    content: Optional[str] = None,
    line_endings: Optional[str] = None
) -> None:
    if name is not None:
        view.set_name(name)

    if content is not None:
        view.run_command('append', {'characters': content})

    if settings is not None:
        view_settings = view.settings()
        for key, value in settings.items():
            view_settings.set(key, value)

    if read_only is not None:
        view.set_read_only(read_only)

    if scratch is not None:
        view.set_scratch(scratch)

    if overwrite is not None:
        view.set_overwrite_status(overwrite)

    if scope is not None:
        view.assign_syntax(get_syntax_for_scope(scope))

    if syntax is not None:
        view.assign_syntax(syntax)

    if encoding is not None:
        view.set_encoding(to_sublime(encoding))

    if line_endings is not None:
        view.set_line_endings(LineEnding(line_endings).name)


VIEW_OPTIONS = {
    name
    for name, param in inspect.signature(set_view_options).parameters.items()
    if param.kind == inspect.Parameter.KEYWORD_ONLY
}
