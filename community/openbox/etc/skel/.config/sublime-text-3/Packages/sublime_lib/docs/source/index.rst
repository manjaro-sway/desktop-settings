:mod:`sublime_lib` API Reference
================================

A utility library for Sublime Text providing a variety of convenience features for other packages to use.

For general documentation, see the `README <https://github.com/SublimeText/sublime_lib>`_.

Most :mod:`sublime_lib` classes and functions rely on
the `Sublime Text API <https://www.sublimetext.com/docs/3/api_reference.html>`_.
As a result, :mod:`sublime_lib` functionality should not be used at import time.
Instead, any initialization should be performed in :func:`plugin_loaded`.

Settings dictionaries
---------------------

.. autoclass:: sublime_lib.SettingsDict
.. autoclass:: sublime_lib.NamedSettingsDict

Output streams and panels
-------------------------

.. autoclass:: sublime_lib.ViewStream
.. autoclass:: sublime_lib.Panel
.. autoclass:: sublime_lib.OutputPanel

Resource paths
--------------

.. autoclass:: sublime_lib.ResourcePath

View utilities
--------------

.. autofunction:: sublime_lib.new_view
.. autofunction:: sublime_lib.close_view
.. autoclass:: sublime_lib.LineEnding

Window utilities
----------------

.. autofunction:: sublime_lib.new_window
.. autofunction:: sublime_lib.close_window
.. autofunction:: sublime_lib.show_selection_panel

Syntax utilities
----------------

.. autofunction:: sublime_lib.list_syntaxes
.. autofunction:: sublime_lib.get_syntax_for_scope

Activity indicator
------------------

.. autoclass:: sublime_lib.ActivityIndicator

:mod:`~sublime_lib.encodings` submodule
---------------------------------------

.. automodule:: sublime_lib.encodings

:mod:`~sublime_lib.flags` submodule
-----------------------------------

.. automodule:: sublime_lib.flags
