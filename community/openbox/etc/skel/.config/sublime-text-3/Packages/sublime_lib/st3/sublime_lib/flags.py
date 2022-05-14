"""
Python enumerations for use with Sublime API methods.

In addition to the standard behavior,
these enumerations' constructors accept the name of an enumerated value as a string:

.. code-block:: python

   >>> PointClass(sublime.DIALOG_YES)
   <DialogResult.YES: 1>
   >>> PointClass("YES")
   <DialogResult.YES: 1>

Descendants of :class:`IntFlag` accept zero or more arguments:

.. code-block:: python

   >>> PointClass("WORD_START", "WORD_END")
   <PointClass.WORD_END|WORD_START: 3>
   >>> PointClass()
   <PointClass.0: 0>

.. versionchanged:: 1.2
    Constructors accept member names
    and `IntFlag` constructors accept multiple arguments.
"""

import sublime

from .vendor.python.enum import IntEnum, IntFlag, EnumMeta
from inspect import getdoc, cleandoc

import operator
import re

from ._util.enum import ExtensibleConstructorMeta, construct_union, construct_with_alternatives

from ._compat.typing import Callable, Optional


__all__ = [
    'DialogResult', 'PointClass', 'FindOption', 'RegionOption',
    'PopupOption', 'PhantomLayout', 'OpenFileOption', 'QuickPanelOption',
    'HoverLocation', 'QueryContextOperator', 'CompletionOptions'
]


def autodoc(prefix: Optional[str] = None) -> Callable[[EnumMeta], EnumMeta]:
    if prefix is None:
        prefix_str = ''
    else:
        prefix_str = prefix + '_'

    def decorator(enum: EnumMeta) -> EnumMeta:
        enum.__doc__ = getdoc(enum) + '\n\n' + '\n'.join([
            cleandoc("""
            .. py:attribute:: {name}
                :annotation: = sublime.{pre}{name}
            """).format(name=item.name, pre=prefix_str) for item in enum
        ])

        return enum

    return decorator


construct_from_name = construct_with_alternatives(
    lambda cls, value: cls.__members__.get(value, None)
)


@autodoc('DIALOG')
@construct_from_name
class DialogResult(IntEnum):
    """
    An :class:`~enum.IntEnum` for use with :func:`sublime.yes_no_cancel_dialog`.
    """
    CANCEL = sublime.DIALOG_CANCEL
    YES = sublime.DIALOG_YES
    NO = sublime.DIALOG_NO


@autodoc('CLASS')
@construct_union
@construct_from_name
class PointClass(IntFlag, metaclass=ExtensibleConstructorMeta):
    """
    An :class:`~enum.IntFlag` for use with several methods of :class:`sublime.View`:

    - :meth:`~sublime.View.classify`
    - :meth:`~sublime.View.find_by_class`
    - :meth:`~sublime.View.expand_by_class`
    """
    WORD_START = sublime.CLASS_WORD_START
    WORD_END = sublime.CLASS_WORD_END
    PUNCTUATION_START = sublime.CLASS_PUNCTUATION_START
    PUNCTUATION_END = sublime.CLASS_PUNCTUATION_END
    SUB_WORD_START = sublime.CLASS_SUB_WORD_START
    SUB_WORD_END = sublime.CLASS_SUB_WORD_END
    LINE_START = sublime.CLASS_LINE_START
    LINE_END = sublime.CLASS_LINE_END
    EMPTY_LINE = sublime.CLASS_EMPTY_LINE


@autodoc()
@construct_union
@construct_from_name
class FindOption(IntFlag, metaclass=ExtensibleConstructorMeta):
    """
    An :class:`~enum.IntFlag` for use with several methods of :class:`sublime.View`:

    - :meth:`~sublime.View.find`
    - :meth:`~sublime.View.find_all`
    """
    LITERAL = sublime.LITERAL
    IGNORECASE = sublime.IGNORECASE


@autodoc()
@construct_union
@construct_from_name
class RegionOption(IntFlag, metaclass=ExtensibleConstructorMeta):
    """
    An :class:`~enum.IntFlag` for use with :meth:`sublime.View.add_regions`.
    """
    DRAW_EMPTY = sublime.DRAW_EMPTY
    HIDE_ON_MINIMAP = sublime.HIDE_ON_MINIMAP
    DRAW_EMPTY_AS_OVERWRITE = sublime.DRAW_EMPTY_AS_OVERWRITE
    DRAW_NO_FILL = sublime.DRAW_NO_FILL
    DRAW_NO_OUTLINE = sublime.DRAW_NO_OUTLINE
    DRAW_SOLID_UNDERLINE = sublime.DRAW_SOLID_UNDERLINE
    DRAW_STIPPLED_UNDERLINE = sublime.DRAW_STIPPLED_UNDERLINE
    DRAW_SQUIGGLY_UNDERLINE = sublime.DRAW_SQUIGGLY_UNDERLINE
    PERSISTENT = sublime.PERSISTENT
    HIDDEN = sublime.HIDDEN


@autodoc()
@construct_union
@construct_from_name
class PopupOption(IntFlag, metaclass=ExtensibleConstructorMeta):
    """
    An :class:`~enum.IntFlag` for use with :meth:`sublime.View.show_popup`.
    """
    COOPERATE_WITH_AUTO_COMPLETE = sublime.COOPERATE_WITH_AUTO_COMPLETE
    HIDE_ON_MOUSE_MOVE = sublime.HIDE_ON_MOUSE_MOVE
    HIDE_ON_MOUSE_MOVE_AWAY = sublime.HIDE_ON_MOUSE_MOVE_AWAY


@autodoc('LAYOUT')
@construct_union
@construct_from_name
class PhantomLayout(IntFlag, metaclass=ExtensibleConstructorMeta):
    """
    An :class:`~enum.IntFlag` for use with :class:`sublime.Phantom`.
    """
    INLINE = sublime.LAYOUT_INLINE
    BELOW = sublime.LAYOUT_BELOW
    BLOCK = sublime.LAYOUT_BLOCK


@autodoc()
@construct_union
@construct_from_name
class OpenFileOption(IntFlag, metaclass=ExtensibleConstructorMeta):
    """
    An :class:`~enum.IntFlag` for use with :meth:`sublime.Window.open_file`.
    """
    ENCODED_POSITION = sublime.ENCODED_POSITION
    TRANSIENT = sublime.TRANSIENT


@autodoc()
@construct_union
@construct_from_name
class QuickPanelOption(IntFlag, metaclass=ExtensibleConstructorMeta):
    """
    An :class:`~enum.IntFlag` for use with :meth:`sublime.Window.show_quick_panel`.
    """
    MONOSPACE_FONT = sublime.MONOSPACE_FONT
    KEEP_OPEN_ON_FOCUS_LOST = sublime.KEEP_OPEN_ON_FOCUS_LOST


@autodoc('HOVER')
@construct_from_name
class HoverLocation(IntEnum):
    """
    An :class:`~enum.IntEnum` for use with
    :func:`sublime_plugin.EventListener.on_hover`.

    .. versionadded:: 1.4
    """
    TEXT = sublime.HOVER_TEXT
    GUTTER = sublime.HOVER_GUTTER
    MARGIN = sublime.HOVER_MARGIN


def regex_match(value: str, operand: str) -> bool:
    expr = r'(?:{})\Z'.format(operand)
    return re.match(expr, value) is not None


def not_regex_match(value: str, operand: str) -> bool:
    return not regex_match(value, operand)


def regex_contains(value: str, operand: str) -> bool:
    return re.search(operand, value) is not None


def not_regex_contains(value: str, operand: str) -> bool:
    return not regex_contains(value, operand)


@autodoc('OP')
@construct_from_name
class QueryContextOperator(IntEnum):
    """
    An :class:`~enum.IntEnum` for use with
    :func:`sublime_plugin.EventListener.on_query_context`.

    .. versionadded:: 1.4

    .. py:method:: apply(value, operand)

        Apply the operation to the given values.

        For regexp operators,
        `operand` should contain the regexp to be tested against the string `value`.

    Example usage:

    .. code-block:: python

        import sublime_plugin
        from sublime_lib.flags import QueryContextOperator

        class MyListener(sublime_plugin.EventListener):
            def on_query_context(self, view, key, operator, operand, match_all):
                if key == "my_example_key":
                    value = get_some_value()
                    return QueryContextOperator(operator).apply(value, operand)
                else:
                    return None
    """
    EQUAL = (sublime.OP_EQUAL, operator.eq)
    NOT_EQUAL = (sublime.OP_NOT_EQUAL, operator.ne)
    REGEX_MATCH = (sublime.OP_REGEX_MATCH, regex_match)
    NOT_REGEX_MATCH = (sublime.OP_NOT_REGEX_MATCH, not_regex_match)
    REGEX_CONTAINS = (sublime.OP_REGEX_CONTAINS, regex_contains)
    NOT_REGEX_CONTAINS = (sublime.OP_NOT_REGEX_CONTAINS, not_regex_contains)

    # _apply_ = None  # type: Callable[[str, str], bool]

    def __new__(cls, value: int, operator: Callable[[str, str], bool]) -> 'QueryContextOperator':
        obj = int.__new__(cls, value)  # type: ignore
        obj._value_ = value
        obj._apply_ = operator
        return obj

    def apply(self, value: str, operand: str) -> bool:
        return self._apply_(value, operand)  # type: ignore


@autodoc()
@construct_union
@construct_from_name
class CompletionOptions(IntFlag, metaclass=ExtensibleConstructorMeta):
    """
    An :class:`~enum.IntFlag` for use with
    :func:`sublime_plugin.EventListener.on_query_completions`.

    .. versionadded:: 1.4
    """
    INHIBIT_WORD_COMPLETIONS = sublime.INHIBIT_WORD_COMPLETIONS
    INHIBIT_EXPLICIT_COMPLETIONS = sublime.INHIBIT_EXPLICIT_COMPLETIONS
