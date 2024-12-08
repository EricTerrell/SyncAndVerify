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
import time
from datetime import timedelta
from BaseTest import BaseTest
from FolderQuickCompare import FolderQuickCompare


class TestFolderQuickCompare(BaseTest):
    _exclusions = []

    def test_compare(self):
        source_path = pathlib.Path(self.get_temp_folder(), 'folders/source')
        destination_path = pathlib.Path(self.get_temp_folder(), 'folders/destination')

        comparison = FolderQuickCompare.compare(source_path, destination_path, TestFolderQuickCompare._exclusions)

        correct_folders_to_delete = ['destination really', 'unique_subfolder_destination']

        self.assertEqual(correct_folders_to_delete, comparison.folders_to_delete)

        correct_folders_to_create = ['source really\\nested\\folder',
                                     'unique_subfolder_source']

        self.assertEqual(correct_folders_to_create, comparison.folders_to_create)

        correct_files_to_delete = ['common_subfolder\\unique-file-destination.txt']

        self.assertEqual(correct_files_to_delete, comparison.files_to_delete)

        correct_files_to_copy = ['common_subfolder\\common-file-2.txt',
                                 'common_subfolder\\unique-file-source.txt',
                                 'file1.txt',
                                 'source really\\nested\\folder\\file.txt',
                                 'unique_subfolder_source\\file.txt']

        self.assertEqual(correct_files_to_copy, sorted(comparison.files_to_copy_metadata.keys()))

    @unittest.skip('integration test')
    def test_compare_actual_folders(self):
        source_root = 'D:'
        dest_root = 'G:\\Backup'

        paths = (
            ('D:\\Repositories', f'{dest_root}\\svn'),
            ('D:\\Dropbox',      f'{dest_root}\\Dropbox'),
            ('D:\\Eric',         f'{dest_root}\\Eric'),
            ('Z:\\Barb',         f'{source_root}\\Barb'),
            ('Z:\\Barb',         f'{dest_root}\\Barb'),
            ('Z:\\Photos',       f'{source_root}\\Photos'),
            ('Z:\\Photos',       f'{dest_root}\\Backup\\Photos'),
            ('Z:\\Media\\DVDs',  f'{dest_root}\\Media\\DVDs'),
            ('D:\\Media',        f'{dest_root}\\Media')
        )

        start_time = time.perf_counter()

        for pair in paths:
            print(f'\nComparing "{pair[0]}" and "{pair[1]}"\n')

            comparison = FolderQuickCompare.compare(pair[0], pair[1], TestFolderQuickCompare._exclusions)

            FolderQuickCompare.display_results(comparison)

        print(f'\nTime to compare all folders: {timedelta(seconds=time.perf_counter() - start_time)}')
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
