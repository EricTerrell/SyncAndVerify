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

        # TODO: assert on results

        self.assertTrue(True)

    @unittest.skip('integration test')
    def test_compare_actual_folders(self):
        paths = (
            ('D:\\Repositories', 'E:\\Backup\\svn'),
            ('D:\\Dropbox', 'E:\\Backup\\Dropbox'),
            ('D:\\Eric', 'E:\\Backup\\Eric'),
            ('Z:\\Barb', 'D:\\Barb'),
            ('Z:\\Barb', 'E:\\Backup\\Barb'),
            ('Z:\\Photos', 'D:\\Photos'),
            ('Z:\\Photos', 'E:\\Backup\\Photos'),
            ('Z:\\Media\\DVDs', 'E:\\Backup\\Media\\DVDs'),
            ('D:\\Media', 'E:\\Backup\\Media')
        )

        start_time = time.perf_counter()

        for pair in paths:
            individual_start_time = time.perf_counter()

            print(f'\nComparing {pair[0]} and {pair[1]}\n')

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
