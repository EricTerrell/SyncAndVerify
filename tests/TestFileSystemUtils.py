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

import unittest
import os
from BaseTest import BaseTest
from FileSystemUtils import FileSystemUtils


class TestFileSystemUtils(BaseTest):
    @unittest.skip('integration test')
    def test_get_file_date_times(self):
        source_file_path = 'D:\\media\\music\\ZZ Top\\Greatest Hits\\11.flac'

        # Capture the file times after the copy. After all, the copy itself will update the last_access_time value.
        (creation_time, last_modification_time, last_access_time) = \
            FileSystemUtils.get_file_date_times(source_file_path)

        print(f'creation_time: {creation_time}')
        print(f'last_modification_time: {last_modification_time}')
        print(f'last_access_time: {last_access_time}')

    def test_set_file_date_times(self):
        creation_time = 1561637788.179921
        last_modification_time = 1407594820.999999
        last_access_time = 1607854408.621261

        root = self.get_temp_folder()
        file_path = 'folders/destination/file1.txt'
        path = os.path.join(root, file_path)

        # Ensure that file current doesn't have desired time stamps.
        (retrieved_creation_time, retrieved_last_modification_time, retrieved_last_access_time) = \
            FileSystemUtils.get_file_date_times(path)

        self.assertNotEqual(creation_time, retrieved_creation_time)
        self.assertNotEqual(last_modification_time, retrieved_last_modification_time)
        self.assertNotEqual(last_access_time, retrieved_last_access_time)

        FileSystemUtils.set_file_date_times(path, creation_time, last_modification_time, last_access_time)

        (retrieved_creation_time, retrieved_last_modification_time, retrieved_last_access_time) = \
            FileSystemUtils.get_file_date_times(path)

        self.assertEqual(int(creation_time), int(retrieved_creation_time))
        self.assertEqual(int(last_modification_time), int(retrieved_last_modification_time))
        self.assertEqual(int(last_access_time), int(retrieved_last_access_time))

    @unittest.skip('integration test')
    def test_volume_to_disc_letter(self):
        drive_letter = FileSystemUtils.label_to_drive_letter('Archived Backup')

        self.assertEqual('F', drive_letter)

    @unittest.skip('integration test')
    def test_file_copy(self):
        FileSystemUtils.copy_file('Z:\\Photos\\Photo Album\\2018\\05\\cortez\\eric\'s pictures\\DSC00513.JPG', 'C:\\temp\\DSC00513.JPG')


if __name__ == '__main__':
    unittest.main()
