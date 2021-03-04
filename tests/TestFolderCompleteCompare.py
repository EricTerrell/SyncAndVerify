"""
  SyncAndVerify
  (C) Copyright 2021, Eric Bergman-Terrell

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
import hashlib
import time
from datetime import timedelta
from BaseTest import BaseTest
from FolderCompleteCompare import FolderCompleteCompare


class TestFolderCompleteCompare(BaseTest):
    def test_compare(self):
        source_path = pathlib.Path(self.get_temp_folder(), 'folders/source')
        destination_path = pathlib.Path(self.get_temp_folder(), 'folders/destination')

        comparison = FolderCompleteCompare.compare(source_path, destination_path)

        FolderCompleteCompare.display_results(comparison)

        self.assertEqual(1, len(comparison.folders_in_both_folders))
        self.assertTrue('\\common_subfolder' in comparison.folders_in_both_folders)

        self.assertEqual(4, len(comparison.folders_in_source_folder_only))
        self.assertTrue('\\source really' in comparison.folders_in_source_folder_only)
        self.assertTrue('\\source really\\nested' in comparison.folders_in_source_folder_only)
        self.assertTrue('\\source really\\nested\\folder' in comparison.folders_in_source_folder_only)
        self.assertTrue('\\unique_subfolder_source' in comparison.folders_in_source_folder_only)

        self.assertEqual(4, len(comparison.folders_in_destination_folder_only))
        self.assertTrue('\\destination really\\nested\\folder' in comparison.folders_in_destination_folder_only)
        self.assertTrue('\\unique_subfolder_destination' in comparison.folders_in_destination_folder_only)
        self.assertTrue('\\destination really' in comparison.folders_in_destination_folder_only)
        self.assertTrue('\\destination really\\nested' in comparison.folders_in_destination_folder_only)

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
            individual_start_time = time.perf_counter()

            print(f'\nComparing "{pair[0]}" and "{pair[1]}"\n')

            comparison = FolderCompleteCompare.compare(pair[0], pair[1])

            FolderCompleteCompare.display_results(comparison)

            print(f'Elapsed Time: {timedelta(seconds=time.perf_counter() - individual_start_time)}')

        print(f'\nTime to compare all folders: {timedelta(seconds=time.perf_counter() - start_time)}')

        self.assertTrue(True)

    """
    {
    'shake_128', 'sha512', 'sha1', 'blake2s', 'shake_256', 'sha224', 'sha3_512', 'sha384', 'blake2b', 'sha3_256', 
    'sha3_224', 'sha256', 'sha3_384', 'md5'
    }
    """

    @unittest.skip('just determine available hash algorithms')
    def test_enumerate_hash_algorithms(self):
        print(hashlib.algorithms_guaranteed)


if __name__ == '__main__':
    unittest.main()
