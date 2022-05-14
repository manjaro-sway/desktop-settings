from sphinx.ext.autodoc.importer import _MockObject

import sys


class MockType(_MockObject):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class SublimeMock:
    Region = MockType('sublime.Region')
    View = MockType('sublime.View')
    Window = MockType('sublime.Window')
    Settings = MockType('sublime.Settings')

    def __getattr__(self, key):
        if key.isupper():
            return hash(key)
        else:
            raise AttributeError(key)


sys.modules[__name__] = SublimeMock()
