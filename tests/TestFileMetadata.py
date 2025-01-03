"""
  SyncAndVerify
  (C) Copyright 2025, Eric Bergman-Terrell

  This file is part of SyncAndVerify.

  SyncAndVerify is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    SyncAndVerify is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    See the GNU General Public License: <http://www.gnu.org/licenses/>.
"""

import os
import unittest
from unittest.mock import Mock
from FileMetadata import FileMetadata
from BaseTest import BaseTest


class TestFileMetadata(BaseTest):
    def test_metadata_retrieval(self):
        root = self.get_temp_folder()
        file_path = 'folders/destination/file1.txt'
        path = os.path.join(root, file_path)

        file_metadata = FileMetadata(root, path)
        self.assertEqual(file_metadata.metadata.st_size, 10)
        self.assertEqual(file_path, file_metadata.path)

    def test_metadata_equal(self):
        root = self.get_temp_folder()
        file_path = 'folders/destination/file1.txt'
        path = os.path.join(root, file_path)

        file_metadata_a = FileMetadata(root, path)
        file_metadata_b = FileMetadata(root, path)

        self.assertTrue(file_metadata_a.files_are_same(file_metadata_b))

    def test_metadata_not_equal(self):
        root = self.get_temp_folder()
        file_path = 'folders/destination/file1.txt'
        path = os.path.join(root, file_path)

        original_metadata = FileMetadata(root, path)

        file_metadata_a = FileMetadata(root, path)
        file_metadata_b = FileMetadata(root, path)

        # st_size different
        file_metadata_a.metadata = TestFileMetadata._get_mock_metadata(original_metadata.metadata)
        file_metadata_a.metadata.st_size = 0

        self.assertFalse(file_metadata_a.files_are_same(file_metadata_b))

        # st_mtime different
        file_metadata_a.metadata = TestFileMetadata._get_mock_metadata(original_metadata.metadata)
        mtime = file_metadata_a.metadata.st_ctime

        file_metadata_a.metadata.st_mtime = mtime + FileMetadata.ACCEPTABLE_TIME_DIFFERENCE + 1

        self.assertFalse(file_metadata_a.files_are_same(file_metadata_b))

    @staticmethod
    def _get_mock_metadata(metadata):
        mock_metadata = Mock()
        mock_metadata.st_size = metadata.st_size
        mock_metadata.st_ctime = metadata.st_ctime
        mock_metadata.st_mtime = metadata.st_mtime

        return mock_metadata


if __name__ == '__main__':
    unittest.main()
