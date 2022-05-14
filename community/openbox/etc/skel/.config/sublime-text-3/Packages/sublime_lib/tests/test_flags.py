import sublime
import sublime_lib.flags as flags

from sublime_lib.vendor.python.enum import IntFlag

from functools import reduce
from unittest import TestCase


class TestFlags(TestCase):

    def _test_enum(self, enum, prefix=''):
        for item in enum:
            self.assertEqual(item, getattr(sublime, prefix + item.name))
            self.assertEqual(item, enum(item.name))

        if issubclass(enum, IntFlag):
            self.assertEqual(
                enum(*[item.name for item in enum]),
                reduce(lambda a, b: a | b, enum)
            )

    def test_flags(self):
        self._test_enum(flags.DialogResult, 'DIALOG_')
        self._test_enum(flags.PointClass, 'CLASS_')
        self._test_enum(flags.PhantomLayout, 'LAYOUT_')
        self._test_enum(flags.HoverLocation, 'HOVER_')
        self._test_enum(flags.QueryContextOperator, 'OP_')

        self._test_enum(flags.FindOption)
        self._test_enum(flags.RegionOption)
        self._test_enum(flags.PopupOption)
        self._test_enum(flags.OpenFileOption)
        self._test_enum(flags.QuickPanelOption)
        self._test_enum(flags.CompletionOptions)

    def test_from_strings(self):
        self.assertEqual(
            flags.RegionOption('DRAW_EMPTY', 'HIDE_ON_MINIMAP'),
            flags.RegionOption.DRAW_EMPTY | flags.RegionOption.HIDE_ON_MINIMAP
        )

    def test_from_strings_empty(self):
        self.assertEqual(
            flags.RegionOption(),
            flags.RegionOption(0)
        )

    def test_query_context_operators(self):
        ops = flags.QueryContextOperator

        tests = [
            ('EQUAL', 'x', 'x', 'y'),
            ('REGEX_MATCH', 'aaa', r'a+', r'a'),
            ('REGEX_CONTAINS', 'aaa', r'a', r'b'),
        ]

        for op, key, success, failure in tests:
            self.assertTrue(ops(op).apply(key, success))
            self.assertFalse(ops(op).apply(key, failure))

            self.assertTrue(ops('NOT_' + op).apply(key, failure))
            self.assertFalse(ops('NOT_' + op).apply(key, success))
