from sublime_lib import ResourcePath

from unittest import TestCase


class TestPureResourcePath(TestCase):

    def test_empty_error(self):
        with self.assertRaises(ValueError):
            ResourcePath("")

    def test_eq(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar.py"),
            ResourcePath("Packages/Foo/bar.py")
        )

    def test_ordering_error(self):
        with self.assertRaises(TypeError):
            ResourcePath("Packages") < 'Packages'

    def test_hash(self):
        self.assertIsInstance(
            hash(ResourcePath("Packages/Foo/bar.py")),
            int
        )

    def test_eq_false(self):
        self.assertNotEqual(
            ResourcePath("Packages/Foo/bar.py"),
            "Packages/Foo/bar.py"
        )

    def test_eq_slash(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar.py"),
            ResourcePath("Packages/Foo/bar.py///")
        )

    def test_str(self):
        self.assertEqual(
            str(ResourcePath("Packages/Foo/bar.py")),
            "Packages/Foo/bar.py"
        )

    def test_repr(self):
        self.assertEqual(
            repr(ResourcePath("Packages/Foo/bar.py")),
            "ResourcePath('Packages/Foo/bar.py')"
        )

    def test_parts(self):
        path = ResourcePath("Packages/Foo/bar.py")
        self.assertEqual(path.parts, ("Packages", "Foo", "bar.py"))

    def test_parent(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar.py").parent,
            ResourcePath("Packages/Foo")
        )

    def test_top_parent(self):
        self.assertEqual(
            ResourcePath("Packages").parent,
            ResourcePath("Packages")
        )

    def test_parents(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar.py").parents,
            (
                ResourcePath("Packages/Foo"),
                ResourcePath("Packages")
            )
        )

    def test_parents_root(self):
        self.assertEqual(
            ResourcePath("Packages").parents,
            ()
        )

    def test_name(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar.py").name,
            'bar.py'
        )

    def test_name_directory(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/").name,
            'Foo'
        )

    def test_suffix(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar.py").suffix,
            '.py'
        )

    def test_suffix_none(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar").suffix,
            ''
        )

    def test_suffix_dots_end(self):
        self.assertEqual(
            ResourcePath("foo...").suffix,
            ""
        )

    def test_suffix_multiple(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar.tar.gz").suffix,
            '.gz'
        )

    def test_suffixes(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar.tar.gz").suffixes,
            ['.tar', '.gz']
        )

    def test_suffixes_none(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar").suffixes,
            []
        )

    def test_suffixes_dotend(self):
        self.assertEqual(
            ResourcePath("foo.bar.").suffixes,
            []
        )

    def test_suffixes_dots(self):
        self.assertEqual(
            ResourcePath("foo.bar...baz").suffixes,
            ['.bar', '.', '.', '.baz']
        )

    def test_stem(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar.py").stem,
            'bar'
        )

    def test_stem_dots_end(self):
        self.assertEqual(
            ResourcePath("foo...").stem,
            "foo..."
        )

    def test_stem_multiple(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar.tar.gz").stem,
            'bar.tar'
        )

    def test_stem_none(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar").stem,
            'bar'
        )

    def test_root(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar").root,
            'Packages'
        )

    def test_package(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar").package,
            'Foo'
        )

    def test_package_none(self):
        self.assertEqual(
            ResourcePath("Packages").package,
            None
        )

    def test_package_cache(self):
        self.assertEqual(
            ResourcePath("Cache/Foo").package,
            'Foo'
        )

    def test_match(self):
        path = ResourcePath("Packages/Foo/bar")

        self.assertTrue(path.match('bar'))
        self.assertTrue(path.match('Foo/bar'))
        self.assertTrue(path.match('Foo/*'))
        self.assertTrue(path.match('Packages/*/bar'))
        self.assertTrue(path.match('Packages/Foo/**/bar'))
        self.assertTrue(path.match("/Packages/Foo/bar"))

        self.assertFalse(path.match('baz'))
        self.assertFalse(path.match('Foo'))
        self.assertFalse(path.match('Packages/*/*/bar'))
        self.assertFalse(path.match('/Foo/bar'))
        self.assertFalse(path.match('ar'))

    def test_joinpath(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/").joinpath('bar/', 'baz/xyzzy'),
            ResourcePath("Packages/Foo/bar/baz/xyzzy")
        )

    def test_joinpath_operator(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/") / 'bar/' / 'baz/xyzzy',
            ResourcePath("Packages/Foo/bar/baz/xyzzy")
        )

    def test_relative_to(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/baz/bar.py").relative_to(
                ResourcePath("Packages/Foo")
            ),
            ('baz', 'bar.py')
        )

    def test_relative_to_same(self):
        self.assertEqual(
            ResourcePath("Packages/Foo").relative_to(
                ResourcePath("Packages/Foo")
            ),
            ()
        )

    def test_relative_to_error(self):
        with self.assertRaises(ValueError):
            ResourcePath("Packages/Foo").relative_to(
                ResourcePath("Packages/Bar")
            )

    def test_with_name(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar.py").with_name('baz.js'),
            ResourcePath("Packages/Foo/baz.js")
        )

    def test_with_name_root(self):
        self.assertEqual(
            ResourcePath("Packages").with_name('Cache'),
            ResourcePath("Cache")
        )

    def test_add_suffix(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar").add_suffix('.py'),
            ResourcePath("Packages/Foo/bar.py")
        )

    def test_remove_suffix(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar.py").remove_suffix(),
            ResourcePath("Packages/Foo/bar")
        )

    def test_remove_suffix_none(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar").remove_suffix(must_remove=False),
            ResourcePath("Packages/Foo/bar")
        )

    def test_remove_suffix_none_error(self):
        with self.assertRaises(ValueError):
            ResourcePath("Packages/Foo/bar").remove_suffix()

    def test_remove_suffix_specified(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar.py").remove_suffix('.py'),
            ResourcePath("Packages/Foo/bar")
        )

    def test_remove_suffix_specified_no_match(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar.py").remove_suffix('.zip', must_remove=False),
            ResourcePath("Packages/Foo/bar.py")
        )

    def test_remove_suffix_specified_no_match_error(self):
        with self.assertRaises(ValueError):
            ResourcePath("Packages/Foo/bar.py").remove_suffix('.zip')

    def test_remove_suffix_specified_no_dot(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar.py").remove_suffix('r.py'),
            ResourcePath("Packages/Foo/ba")
        )

    def test_remove_suffix_specified_entire_name(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar.py").remove_suffix('bar.py', must_remove=False),
            ResourcePath("Packages/Foo/bar.py")
        )

    def test_remove_suffix_specified_entire_name_error(self):
        with self.assertRaises(ValueError):
            ResourcePath("Packages/Foo/bar.py").remove_suffix('bar.py')

    def test_remove_suffix_multiple(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar.py").remove_suffix(['.zip', '.py']),
            ResourcePath("Packages/Foo/bar")
        )

    def test_remove_suffix_multiple_matches(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar.tar.gz").remove_suffix(['.tar.gz', '.gz']),
            ResourcePath("Packages/Foo/bar")
        )

    def test_remove_suffix_multiple_matches_backward(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar.tar.gz").remove_suffix(['.gz', '.tar.gz']),
            ResourcePath("Packages/Foo/bar")
        )

    def test_with_suffix(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar.tar.gz").with_suffix('.bz2'),
            ResourcePath("Packages/Foo/bar.tar.bz2")
        )

    def test_with_suffix_empty(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar").with_suffix('.py'),
            ResourcePath("Packages/Foo/bar.py")
        )

    def test_with_suffix_remove(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar.py").with_suffix(''),
            ResourcePath("Packages/Foo/bar")
        )

    def test_with_suffix_root(self):
        self.assertEqual(
            ResourcePath("Packages").with_suffix('.bz2'),
            ResourcePath("Packages.bz2")
        )
