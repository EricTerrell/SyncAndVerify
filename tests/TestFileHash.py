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
import hashlib
from FileHash import FileHash
from BaseTest import BaseTest


class TestFileHash(BaseTest):
    _exclusions = []

    def test_hash(self):
        root = self.get_temp_folder()
        file_path = 'folders/destination/file1.txt'
        full_file_path = os.path.join(root, file_path)

        file_hash = FileHash().create_file_hash(full_file_path)

        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(b'hello eric')
        expected_result = hash_algorithm.hexdigest()

        self.assertEqual(expected_result, file_hash)

    def test_hash_with_large_file(self):
        root = self.get_temp_folder()
        file_path = 'photo.jpg'
        full_file_path = os.path.join(root, file_path)

        # From Linux sha256sum command
        expected_hash = 'cf20ac3f8aa414fd74d1de103c9672a768b350f6a1f1415964d42f3330a7f88f'

        actual_hash = FileHash().create_file_hash(full_file_path)

        self.assertEqual(expected_hash, actual_hash)


if __name__ == '__main__':
    unittest.main()
