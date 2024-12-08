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
import os
import unittest
import shutil
from BaseTest import BaseTest
from FolderSync import FolderSync
from FolderCompleteCompare import FolderCompleteCompare
from FolderQuickCompare import FolderQuickCompare


class TestErrorHandling(BaseTest):
    @unittest.skip('integration test')
    def test_ignore_specified_errors(self):
        source_path = 'C:\\Users\\Eric Terrell\\Dropbox'
        destination_path = 'I:\\Dropbox'
        exclusions = ['.dropbox.cache', '__EXCLUDE__\\__ME__']

        if os.path.isdir(destination_path):
            shutil.rmtree(destination_path, onerror=FolderSync._delete_readonly_file)

        os.mkdir(destination_path)

        comparison = FolderQuickCompare.compare(source_path, destination_path, exclusions)

        self.assertTrue(len(comparison.folders_to_create) == 47)
        self.assertTrue(len(comparison.folders_to_delete) == 0)
        self.assertTrue(len(comparison.files_to_delete) == 0)
        self.assertTrue(len(comparison.files_to_copy_metadata) == 704)

        FolderSync.sync(source_path, destination_path, exclusions)

        comparison = FolderQuickCompare.compare(source_path, destination_path, exclusions)

        self.assertTrue(len(comparison.folders_to_create) == 0)
        self.assertTrue(len(comparison.folders_to_delete) == 0)
        self.assertTrue(len(comparison.files_to_delete) == 0)
        self.assertTrue(len(comparison.files_to_copy_metadata) == 0)

        comparison = FolderCompleteCompare.compare(source_path, destination_path, exclusions)

        self.assertTrue(len(comparison.files_in_source_folder_only) == 0)
        self.assertTrue(len(comparison.files_in_destination_folder_only) == 0)
        self.assertTrue(len(comparison.files_in_both_folders) == 704)
        self.assertTrue(len(comparison.different_files) == 0)
        self.assertTrue(len(comparison.could_not_read_files) == 0)
        self.assertTrue(len(comparison.source_hashes) == len(comparison.files_in_both_folders))
        self.assertTrue(len(comparison.destination_hashes) == len(comparison.files_in_both_folders))


if __name__ == '__main__':
    unittest.main()
