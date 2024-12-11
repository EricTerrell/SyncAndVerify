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
from FolderMetadata import FolderMetadata
from BaseTest import BaseTest


class TestFolderMetadata(BaseTest):
    _exclusions = []

    def test_metadata_retrieval(self):
        folder_metadata = FolderMetadata(self.get_temp_folder(), TestFolderMetadata._exclusions)

        metadata = folder_metadata.get_metadata()

        folders = metadata[0]
        files = metadata[1]

        print(f'Root: {folder_metadata.root}')
        print(f'folder count: {len(folders)}')
        print(f'file count: {len(files)}')
        print()

        for folder in folders:
            print(f'Folder: {folder}')

        print()

        for file in files:
            print(f'File: {files[file].path} Size: {files[file].metadata.st_size} Creation Time: {files[file].metadata.st_ctime} Last Modification Time: {files[file].metadata.st_mtime} Last Access Time: {files[file].metadata.st_atime}')

        self.assertTrue(self, True)


if __name__ == '__main__':
    unittest.main()
