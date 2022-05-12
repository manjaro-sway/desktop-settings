from sublime_lib._util.simple_yaml import parse_simple_top_level_keys

from unittest import TestCase


TEXT = r"""
# A comment
'single': 'test '' value'
"double": "test\nvalue"
unquoted: test\value
true: true
false: false
null: null
multiline:
  not: parsed
"""


class TestSettingsDict(TestCase):

    def test_parse_simple_top_level_keys(self):
        self.assertEqual(
            parse_simple_top_level_keys(TEXT),
            {
                'single': 'test \' value',
                'double': 'test\nvalue',
                'unquoted': 'test\\value',
                True: True,
                False: False,
                None: None,
            }
        )
