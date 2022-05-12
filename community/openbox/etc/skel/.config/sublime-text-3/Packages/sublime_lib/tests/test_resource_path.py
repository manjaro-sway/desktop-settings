import sublime
import shutil
import tempfile

from sublime_lib import ResourcePath
from sublime_lib._compat.pathlib import Path

from unittesting import DeferrableTestCase


class TestResourcePath(DeferrableTestCase):

    def setUp(self):
        shutil.copytree(
            src=str(ResourcePath("Packages/sublime_lib/tests/test_package").file_path()),
            dst=str(ResourcePath("Packages/test_package").file_path()),
        )

        yield ResourcePath("Packages/test_package/.test_package_exists").exists

    def tearDown(self):
        shutil.rmtree(
            str(ResourcePath("Packages/test_package").file_path()),
            ignore_errors=True
        )

    def test_glob_resources(self):
        self.assertEqual(
            ResourcePath.glob_resources("Packages/test_package/*.txt"),
            [
                ResourcePath("Packages/test_package/helloworld.txt"),
                ResourcePath("Packages/test_package/UTF-8-test.txt"),
            ]
        )

        self.assertEqual(
            ResourcePath.glob_resources("ks27jArEz4"),
            []
        )

        self.assertEqual(
            ResourcePath.glob_resources("*ks27jArEz4"),
            [
                ResourcePath('Packages/sublime_lib/tests/uniquely_named_file_ks27jArEz4')
            ]
        )

    def test_from_file_path_packages(self):
        self.assertEqual(
            ResourcePath.from_file_path(Path(sublime.packages_path(), 'test_package')),
            ResourcePath("Packages/test_package")
        )

    def test_from_file_path_cache(self):
        self.assertEqual(
            ResourcePath.from_file_path(Path(sublime.cache_path(), 'test_package')),
            ResourcePath("Cache/test_package")
        )

    def test_from_file_path_installed_packages(self):
        self.assertEqual(
            ResourcePath.from_file_path(
                Path(sublime.installed_packages_path(), 'test_package.sublime-package', 'foo.py')
            ),
            ResourcePath("Packages/test_package/foo.py")
        )

    def test_from_file_path_installed_packages_not_installed(self):
        with self.assertRaises(ValueError):
            ResourcePath.from_file_path(
                Path(sublime.installed_packages_path(), 'test_package', 'foo.py')
            ),

    def test_from_file_path_installed_packages_root(self):
        self.assertEqual(
            ResourcePath.from_file_path(Path(sublime.installed_packages_path())),
            ResourcePath("Packages")
        )

    def test_from_file_path_default_packages(self):
        self.assertEqual(
            ResourcePath.from_file_path(
                Path(sublime.executable_path()).parent.joinpath(
                    'Packages', 'test_package.sublime-package', 'foo.py'
                )
            ),
            ResourcePath("Packages/test_package/foo.py")
        )

    def test_from_file_path_default_packages_root(self):
        self.assertEqual(
            ResourcePath.from_file_path(
                Path(sublime.executable_path()).parent / 'Packages'
            ),
            ResourcePath("Packages")
        )

    def test_from_file_path_error(self):
        with self.assertRaises(ValueError):
            ResourcePath.from_file_path(Path('/test_package')),

    def test_from_file_path_relative(self):
        with self.assertRaises(ValueError):
            ResourcePath.from_file_path(Path('test_package')),

    def test_file_path_packages(self):
        self.assertEqual(
            ResourcePath("Packages/Foo/bar.py").file_path(),
            Path(sublime.packages_path(), 'Foo/bar.py')
        )

    def test_file_path_packages_root(self):
        self.assertEqual(
            ResourcePath("Packages").file_path(),
            Path(sublime.packages_path())
        )

    def test_file_path_cache(self):
        self.assertEqual(
            ResourcePath("Cache/Foo/bar.py").file_path(),
            Path(sublime.cache_path(), 'Foo/bar.py')
        )

    def test_file_path_error(self):
        with self.assertRaises(ValueError):
            ResourcePath("Elsewhere/Foo/bar.py").file_path(),

    def test_exists(self):
        self.assertTrue(
            ResourcePath("Packages/test_package/helloworld.txt").exists()
        )

    def test_not_exists(self):
        self.assertFalse(
            ResourcePath("Packages/test_package/nonexistentfile.txt").exists()
        )

    def test_read_text(self):
        self.assertEqual(
            ResourcePath("Packages/test_package/helloworld.txt").read_text(),
            "Hello, World!\n"
        )

    def test_read_text_missing(self):
        with self.assertRaises(FileNotFoundError):
            ResourcePath("Packages/test_package/nonexistentfile.txt").read_text()

    def test_read_text_invalid_unicode(self):
        with self.assertRaises(UnicodeDecodeError):
            ResourcePath("Packages/test_package/UTF-8-test.txt").read_text()

    def test_read_bytes(self):
        self.assertEqual(
            ResourcePath("Packages/test_package/helloworld.txt").read_bytes(),
            b"Hello, World!\n"
        )

    def test_read_bytes_missing(self):
        with self.assertRaises(FileNotFoundError):
            ResourcePath("Packages/test_package/nonexistentfile.txt").read_bytes()

    def test_read_bytes_invalid_unicode(self):
        # Should not raise UnicodeDecodeError
        ResourcePath("Packages/test_package/UTF-8-test.txt").read_bytes()

    def test_glob(self):
        self.assertEqual(
            ResourcePath("Packages/test_package").glob('*.txt'),
            [
                ResourcePath("Packages/test_package/helloworld.txt"),
                ResourcePath("Packages/test_package/UTF-8-test.txt"),
            ]
        )

    def test_rglob(self):
        self.assertEqual(
            ResourcePath("Packages/test_package").rglob('*.txt'),
            [
                ResourcePath("Packages/test_package/helloworld.txt"),
                ResourcePath("Packages/test_package/UTF-8-test.txt"),
                ResourcePath("Packages/test_package/directory/goodbyeworld.txt"),
            ]
        )

    def test_rglob_error(self):
        with self.assertRaises(NotImplementedError):
            ResourcePath("Packages/test_package").rglob('/*.txt')

    def test_children(self):
        self.assertEqual(
            ResourcePath("Packages/test_package").children(),
            [
                ResourcePath("Packages/test_package/.test_package_exists"),
                ResourcePath("Packages/test_package/helloworld.txt"),
                ResourcePath("Packages/test_package/UTF-8-test.txt"),
                ResourcePath("Packages/test_package/directory"),
            ]
        )

    def test_copy_text(self):
        with tempfile.TemporaryDirectory() as directory:
            source = ResourcePath("Packages/test_package/helloworld.txt")
            destination = Path(directory) / 'helloworld.txt'

            source.copy(destination)

            self.assertTrue(destination.is_file())

            with open(str(destination), 'r') as file:
                text = file.read()

            self.assertEqual(text, source.read_text())

    def test_copy_binary(self):
        with tempfile.TemporaryDirectory() as directory:
            source = ResourcePath("Packages/test_package/UTF-8-test.txt")
            destination = Path(directory) / 'UTF-8-test.txt'

            source.copy(destination)

            self.assertTrue(destination.is_file())

            with open(str(destination), 'rb') as file:
                data = file.read()

            self.assertEqual(data, source.read_bytes())

    def test_copy_existing(self):
        with tempfile.TemporaryDirectory() as directory:
            source = ResourcePath("Packages/test_package/helloworld.txt")
            destination = Path(directory) / 'helloworld.txt'

            with open(str(destination), 'w') as file:
                file.write("Nothing to see here.\n")

            source.copy(destination)

            self.assertTrue(destination.is_file())

            with open(str(destination), 'r') as file:
                text = file.read()

            self.assertEqual(text, source.read_text())

    def test_copy_existing_error(self):
        with tempfile.TemporaryDirectory() as directory:
            source = ResourcePath("Packages/test_package/helloworld.txt")
            destination = Path(directory) / 'helloworld.txt'

            text = "Nothing to see here.\n"
            with open(str(destination), 'w') as file:
                file.write(text)

            with self.assertRaises(FileExistsError):
                source.copy(destination, False)

    def test_copy_directory_error(self):
        with tempfile.TemporaryDirectory() as directory:
            source = ResourcePath("Packages/test_package/helloworld.txt")
            destination = Path(directory) / 'helloworld.txt'

            destination.mkdir()

            with self.assertRaises(IsADirectoryError):
                source.copy(destination)

            self.assertTrue(destination.is_dir())

    def test_copytree(self):
        with tempfile.TemporaryDirectory() as directory:
            source = ResourcePath("Packages/test_package")
            destination = Path(directory) / 'tree'

            source.copytree(destination)

            self.assertEqual(
                {
                    path.relative_to(destination).parts
                    for path in destination.rglob('*')
                    if path.is_file()
                },
                {
                    path.relative_to(source)
                    for path in source.rglob('*')
                }
            )

    def test_copytree_exists_error(self):
        with tempfile.TemporaryDirectory() as directory:
            source = ResourcePath("Packages/test_package")
            destination = Path(directory) / 'tree'
            destination.mkdir()

            with self.assertRaises(FileExistsError):
                source.copytree(destination)

    def test_copytree_exists(self):
        with tempfile.TemporaryDirectory() as directory:
            source = ResourcePath("Packages/test_package")
            destination = Path(directory) / 'tree'
            destination.mkdir()

            helloworld_file = destination / 'helloworld.txt'

            with open(str(helloworld_file), 'w') as file:
                file.write("Nothing to see here.\n")

            source.copytree(destination, exist_ok=True)

            self.assertEqual(
                {
                    path.relative_to(destination).parts
                    for path in destination.rglob('*')
                    if path.is_file()
                },
                {
                    path.relative_to(source)
                    for path in source.rglob('*')
                }
            )

            with open(str(helloworld_file)) as file:
                helloworld_contents = file.read()

            self.assertEqual(
                helloworld_contents,
                (source / 'helloworld.txt').read_text()
            )
