from sublime_lib._util.glob import get_glob_matcher

from unittest import TestCase


class TestGlob(TestCase):
    def _test_matches(self, pattern, positive, negative):
        matcher = get_glob_matcher(pattern)

        for path in positive:
            if not matcher(path):
                raise self.failureException(
                    "{!r} does not match {!r}".format(pattern, path)
                )

        for path in negative:
            if matcher(path):
                raise self.failureException(
                    "{!r} matches {!r}".format(pattern, path)
                )

    def test_recursive_invalid(self):
        with self.assertRaises(ValueError):
            get_glob_matcher('foo**')

    def test_basic(self):
        self._test_matches(
            '/Packages/Foo/bar',
            [
                'Packages/Foo/bar',
            ],
            [
                'Packages/Foo',
                'Packages/Foo/barr',
                'Packages/Foo/bar/baz',
            ]
        )

        self._test_matches(
            'Foo/bar',
            [
                'Foo/bar',
                'Packages/Foo/bar',
            ],
            [
                'Packages/Foo/bar/baz',
                'FooFoo/bar',
            ]
        )

    def test_star(self):
        self._test_matches(
            '/Packages/Foo/*',
            [
                'Packages/Foo/bar',
            ],
            [
                'Packages/Foo',
                'Packages/Foo/bar/baz',
            ]
        )

        self._test_matches(
            'Foo/*',
            [
                'Packages/Foo/bar',
            ],
            [
                'Packages/Foo',
                'Packages/Foo/bar/baz',
            ]
        )

        self._test_matches(
            '/Packages/Foo/A*Z',
            [
                'Packages/Foo/AZ',
                'Packages/Foo/AfoobarZ',
                'Packages/Foo/AAAZZZ',
            ],
            [
                'Packages/Foo/AZbar',
                'Packages/Foo/AZ/bar',
                'Packages/Foo/A/Z',
            ]
        )

        self._test_matches(
            'Foo/A*Z',
            [
                'Packages/Foo/AZ',
                'Packages/Foo/AfoobarZ',
                'Packages/Foo/AAAZZZ',
            ],
            [
                'Packages/Foo/AZbar',
                'Packages/Foo/AZ/bar',
                'Packages/Foo/A/Z',
            ]
        )

    def test_recursive(self):
        self._test_matches(
            '/Packages/Foo/**',
            [
                'Packages/Foo/bar',
                'Packages/Foo/bar/baz',
            ],
            [
                'Packages/Foo',
                'Packages/Foobar',
            ]
        )

        self._test_matches(
            'Foo/**',
            [
                'Packages/Foo/bar',
                'Packages/Foo/bar/baz',
            ],
            [
                'Packages/Foo',
                'Packages/Foobar',
            ]
        )

        self._test_matches(
            '/Packages/Foo/**/bar',
            [
                'Packages/Foo/bar',
                'Packages/Foo/xyzzy/bar',
            ],
            [
                'Packages/Foo/bar/baz',
            ]
        )

        self._test_matches(
            'Foo/**/bar',
            [
                'Packages/Foo/bar',
                'Packages/Foo/xyzzy/bar',
            ],
            [
                'Packages/Foo/bar/baz',
            ]
        )

        self._test_matches(
            '/**/Packages/Foo/bar',
            [
                'Packages/Foo/bar',
            ],
            []
        )

    def test_placeholder(self):
        self._test_matches(
            '/Packages/Foo/ba?',
            [
                'Packages/Foo/bar',
                'Packages/Foo/baz',
            ],
            [
                'Packages/Foo/bar/baz',
            ]
        )

    def test_range(self):
        self._test_matches(
            '/Packages/Foo/ba[rz]',
            [
                'Packages/Foo/bar',
                'Packages/Foo/baz',
            ],
            [
                'Packages/Foo/bar/baz',
                'Packages/Foo/barr',
                'Packages/Foo/bat',
            ]
        )

        self._test_matches(
            '/Packages/Foo/ba[a-z]',
            [
                'Packages/Foo/bar',
                'Packages/Foo/baz',
            ],
            [
                '/Packages/Foo/baR',
            ]
        )
