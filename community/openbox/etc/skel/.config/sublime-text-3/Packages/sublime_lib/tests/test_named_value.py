from sublime_lib._util.named_value import NamedValue

from unittest import TestCase


class TestNamedValue(TestCase):

    def test_named_value(self):
        s = "Hello, World!"
        self.assertEqual(
            repr(NamedValue(s)),
            s
        )
