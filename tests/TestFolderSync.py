"""
  SyncAndVerify
  (C) Copyright 2024, Eric Bergman-Terrell

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

import unittest
import pathlib
from BaseTest import BaseTest
from FolderSync import FolderSync
from FolderMetadata import FolderMetadata
from FolderCompleteCompare import FolderCompleteCompare
from FolderQuickCompare import FolderQuickCompare


class TestFolderSync(BaseTest):
    _exclusions = []

    def test_sync(self):
        source_path = pathlib.Path(self.get_temp_folder(), 'folders/source')
        destination_path = pathlib.Path(self.get_temp_folder(), 'folders/destination')

        FolderSync.sync(source_path, destination_path, TestFolderSync._exclusions)

        source_folder_metadata = FolderMetadata(source_path, TestFolderSync._exclusions)
        destination_folder_metadata = FolderMetadata(destination_path, TestFolderSync._exclusions)

        source_metadata = source_folder_metadata.get_metadata()
        destination_metadata = destination_folder_metadata.get_metadata()

        self.assertEqual(len(source_metadata[0]), len(destination_metadata[0]))
        self.assertEqual(len(source_metadata[1]), len(destination_metadata[1]))

    @unittest.skip('integration test')
    def test_sync_actual_folder(self):
        source_path = 'Z:\\Photos'
        destination_path = 'F:\\backup-test\\Photos'

        FolderSync.sync(source_path, destination_path, TestFolderSync._exclusions)

        comparison = FolderQuickCompare.compare(source_path, destination_path, TestFolderSync._exclusions)

        self.assertTrue(len(comparison.folders_to_create) == 0)
        self.assertTrue(len(comparison.folders_to_delete) == 0)
        self.assertTrue(len(comparison.files_to_delete) == 0)
        self.assertTrue(len(comparison.files_to_copy_metadata) == 0)

        comparison = FolderCompleteCompare.compare(source_path, destination_path, TestFolderSync._exclusions)

        self.assertTrue(len(comparison.files_in_source_folder_only) == 0)
        self.assertTrue(len(comparison.files_in_destination_folder_only) == 0)
        self.assertTrue(len(comparison.files_in_both_folders) > 0)
        self.assertTrue(len(comparison.different_files) == 0)
        self.assertTrue(len(comparison.could_not_read_files) == 0)
        self.assertTrue(len(comparison.source_hashes) == len(comparison.files_in_both_folders))
        self.assertTrue(len(comparison.destination_hashes) == len(comparison.files_in_both_folders))


if __name__ == '__main__':
    unittest.main()
