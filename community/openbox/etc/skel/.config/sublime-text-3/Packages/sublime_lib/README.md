# sublime_lib

A utility library for Sublime Text providing a variety of convenience features for other packages to use.

## Installation

To make use of sublime_lib in your own package, first declare it as a [dependency](https://packagecontrol.io/docs/dependencies) of your package. Create a file named `dependencies.json` in the root of your package with the following contents:

```json
{
    "*": {
        "*": [
            "sublime_lib"
        ]
    }
}
```

Once you have declared the dependency, open the command palette and run `Package Control: Satisfy Dependencies` to ensure that sublime_lib is installed and available for use.

Then, anywhere in your package, you can import sublime_lib by name:

```python
import sublime_lib
```

## Features

For complete documentation of all features, see the [API documentation](https://sublimetext.github.io/sublime_lib/).

Highlights include:

- [`SettingsDict`](https://sublimetext.github.io/sublime_lib/modules/sublime_lib.settings_dict.html), which wraps a `sublime.Settings` object with an interface modeled after a standard Python `dict`.
- [`ViewStream`](https://sublimetext.github.io/sublime_lib/modules/sublime_lib.view_stream.html), a standard [Python IO stream](https://docs.python.org/3/library/io.html#io.TextIOBase) wrapping a `sublime.View` object; and [OutputPanel](https://sublimetext.github.io/sublime_lib/modules/sublime_lib.output_panel.html), which extends `ViewStream` to provide additional functionality for output panel views.
- The [`syntax` submodule](https://sublimetext.github.io/sublime_lib/modules/sublime_lib.syntax.html), providing methods to list all loaded syntax definitions and to find a syntax matching a given scope.
