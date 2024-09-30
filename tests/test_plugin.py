import os
import posixpath
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock

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
                {'File1': 'dir1/file1.md'},
                {'File2': 'dir1/file2.md'}
            ]},
            {'Dir2': [
                {'Sub Dir1': [
                    {'File3': 'dir2/sub-dir1/file3.md'}
                ]}
            ]}
        ]
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
                {'File2': '01_dir2/file2.md'},
                {'File3': '01_dir2/file3.md'}
            ]},
            {'Dir1': [
                {'File12': '02_dir1/00_file12.md'},
                {'File1': '02_dir1/99_file1.md'}
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
                {'Index': 'blog/index.md'}
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
                {'Index': '00_blog/index.md'}
            ]},
            {'A Second Menu': [
                {'Index': '01_a-second-menu/index.md'}
            ]},
            {'C Menu': [
                {'Index': 'c-menu/index.md'},
                {'Sub C Menu': 'c-menu/sub-c-menu.md'}
            ]},
            {'D Menu': 'd-menu.md'},
        ]
        self.assertEqual(result, expected_result)

    def test_on_files_with_valid_files(self):
        files = [
            Mock(dest_path="01_file.md", dest_uri="01_file.md", url="01_file.md",
                 abs_dest_path=os.path.join('abs', 'path', '01_file.md')),
            Mock(dest_path="02_file.md", dest_uri="02_file.md", url="02_file.md",
                 abs_dest_path=os.path.join('abs', 'path', '02_file.md'))
        ]
        config = {}
        result = self.plugin.on_files(files, config)
        self.assertEqual(result[0].dest_path, "file.md")
        self.assertEqual(result[0].dest_uri, "file.md")
        self.assertEqual(result[0].url, "file.md")
        self.assertEqual(result[0].abs_dest_path,
                         os.path.join('abs', 'path', 'file.md'))
        self.assertEqual(result[1].dest_path, "file.md")
        self.assertEqual(result[1].dest_uri, "file.md")
        self.assertEqual(result[1].url, "file.md")
        self.assertEqual(result[1].abs_dest_path,
                         os.path.join('abs', 'path', 'file.md'))

    def test_on_files_with_no_files(self):
        files = []
        config = {}
        result = self.plugin.on_files(files, config)
        self.assertEqual(result, [])

    def test_on_files_with_non_digit_prefix(self):
        files = [
            Mock(dest_path="ab_file.md", dest_uri="ab_file.md", url="ab_file.md",
                 abs_dest_path=os.path.join('abs', 'path', 'ab_file.md'))
        ]
        config = {}
        result = self.plugin.on_files(files, config)
        self.assertEqual(result[0].dest_path, "ab_file.md")
        self.assertEqual(result[0].dest_uri, "ab_file.md")
        self.assertEqual(result[0].url, "ab_file.md")
        self.assertEqual(result[0].abs_dest_path,
                         os.path.join('abs', 'path', 'ab_file.md'))

    def test_on_files_with_posix_path_separator_on_url(self):
        files = [
            Mock(dest_path=os.path.join('dir', 'ab_file.md'),
                 dest_uri=posixpath.join('dir', 'ab_file.md'),
                 url=posixpath.join('dir', 'ab_file.md'),
                 abs_dest_path=os.path.join('abs', 'dir', 'ab_file.md'))
        ]
        config = {}
        result = self.plugin.on_files(files, config)
        self.assertEqual(result[0].dest_path, os.path.join('dir', 'ab_file.md'))
        self.assertEqual(result[0].dest_uri, "dir/ab_file.md")
        self.assertEqual(result[0].url, "dir/ab_file.md")
        self.assertEqual(result[0].abs_dest_path,
                         os.path.join('abs', 'dir', 'ab_file.md'))


if __name__ == '__main__':
    unittest.main()
