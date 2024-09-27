import os
import posixpath
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from mkdocs_gen_nav_plugin.plugin import GenNavPlugin
from tests.testutil import create_dirs_and_files_from_yaml


class TestGenNavPluginStaticMethods(unittest.TestCase):

    def test_format_title(self):
        assert GenNavPlugin.format_title("hello-world") == "Hello World"
        assert GenNavPlugin.format_title("hello_world") == "Hello World"
        assert GenNavPlugin.format_title("hello") == "Hello"
        assert GenNavPlugin.format_title("hello-there") == "Hello There"
        assert GenNavPlugin.format_title("hello_there") == "Hello There"
        assert GenNavPlugin.format_title("hello-there-world") == "Hello There World"
        assert GenNavPlugin.format_title("hello_there_world") == "Hello There World"

    def test_remove_prefix_with_short_string(self):
        self.assertEqual(GenNavPlugin.remove_prefix("a"), "a")
        self.assertEqual(GenNavPlugin.remove_prefix("7"), "7")

    def test_remove_prefix_with_digit(self):
        self.assertEqual(GenNavPlugin.remove_prefix("01_item"), "item")

    def test_remove_prefix_without_digit(self):
        self.assertEqual(GenNavPlugin.remove_prefix("item"), "item")

    def test_remove_prefix_with_non_digit_prefix(self):
        self.assertEqual(GenNavPlugin.remove_prefix("ab_item"), "ab_item")


class TestGenNavPlugin(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.root_path = self.temp_dir.name
        self.plugin = GenNavPlugin()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_nav_dict_listfiles(self):
        structure = """
        dir1:
          - file1.md
          - file2.md
        dir2:
          sub-dir1:
            - file3.md
        """
        self.temp_dir = create_dirs_and_files_from_yaml(self.temp_dir, structure)

        # testing
        result = self.plugin.create_nav_dict(self.root_path, self.root_path, '.md')
        expected_result = [
            {'Dir1': [
                {'File1': posixpath.join('dir1', 'file1.md')},
                {'File2': posixpath.join('dir1', 'file2.md')}
            ]},
            {'Dir2': [
                {'Sub Dir1': [
                    {'File3': posixpath.join('dir2', 'sub-dir1', 'file3.md')}
                ]}
            ]}
        ]
        print(result)
        self.assertEqual(result, expected_result)

    def test_create_nav_dict_orderedList(self):
        structure = """
        02_dir1:
          - 99_file1.md
          - 00_file12.md
        01_dir2:
          - file3.md
          - _ignore.md
          - file2.md
        """
        self.temp_dir = create_dirs_and_files_from_yaml(self.temp_dir, structure)

        # testing
        result = self.plugin.create_nav_dict(self.root_path, self.root_path, '.md')
        expected_result = [
            {'Dir2': [
                {'File2': posixpath.join('01_dir2', 'file2.md')},
                {'File3': posixpath.join('01_dir2', 'file3.md')}
            ]},
            {'Dir1': [
                {'File12': posixpath.join('02_dir1', '00_file12.md')},
                {'File1': posixpath.join('02_dir1', '99_file1.md')}
            ]}
        ]
        self.assertEqual(result, expected_result)

    def test_create_nav_dict_index(self):
        structure = """
        - index.md
        - blog:
          - _posts:
            - 2019-01-01.md
            - 2019-01-02.md
          - index.md
        """
        self.temp_dir = create_dirs_and_files_from_yaml(self.temp_dir, structure)

        # testing
        result = self.plugin.create_nav_dict(self.root_path, self.root_path, '.md')
        expected_result = [
            {'Blog': [
                {'Index': posixpath.join('blog', 'index.md')}
            ]}
        ]
        self.assertEqual(result, expected_result)

    def test_create_nav_dict_example_with_material(self):
        test_dir = os.path.split(__file__)[0]
        test_path = Path(test_dir) / ".." / "examples" / "example-with-material" / "docs"

        # testing
        result = self.plugin.create_nav_dict(test_path, test_path, '.md')
        expected_result = [
            {'Blog': [
                {'Index': posixpath.join('00_blog', 'index.md')}
            ]},
            {'A Second Menu': [
                {'Index': posixpath.join('01_a-second-menu', 'index.md')}
            ]},
            {'C Menu': [
                {'Index': posixpath.join('c-menu', 'index.md')},
                {'Sub C Menu': posixpath.join('c-menu', 'sub-c-menu.md')}
            ]},
            {'D Menu': posixpath.join('d-menu.md')},
        ]
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
