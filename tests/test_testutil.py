import os.path
import tempfile
import unittest
from pathlib import Path

from tests.testutil import create_dirs_and_files_from_yaml


class TestCreateDirsAndFilesFromYaml(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root_path = self.temp_dir.name

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_flat_structure(self):
        structure = """
        - file1.txt
        - file2.txt
        - file3.txt
        """
        base_dir = create_dirs_and_files_from_yaml(self.temp_dir, structure)
        self.assertTrue(os.path.isfile(Path(base_dir.name, 'file1.txt')))
        self.assertTrue(os.path.isfile(Path(base_dir.name, 'file2.txt')))
        self.assertTrue(os.path.isfile(Path(base_dir.name, 'file3.txt')))

    def test_nested_structure(self):
        structure = """
        dir1:
          - file1.txt
        dir2:
          dir3:
            - file2.txt
        """
        base_dir = create_dirs_and_files_from_yaml(self.temp_dir, structure)
        self.assertTrue(os.path.isfile(Path(base_dir.name, 'dir1', 'file1.txt')))
        self.assertTrue(os.path.isfile(Path(base_dir.name, 'dir2', 'dir3', 'file2.txt')))


if __name__ == '__main__':
    unittest.main()
