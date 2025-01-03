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
from FileMetadata import FileMetadata
from FileSystemUtils import FileSystemUtils
from AppException import AppException


class FolderMetadata:
    def __init__(self, root, exclusions):
        self.root = FileSystemUtils.canonical_folder_path(root)
        self.exclusions = exclusions

    def get_metadata(self):
        folders = []

        walk = os.walk(self.root, True, self._error)

        for dir_path, dir_names, file_names in walk:
            for dir_name in dir_names:
                folder = os.path.join(dir_path, dir_name)
                folder = folder[len(self.root):len(folder)]

                if not FolderMetadata._folder_excluded(self, folder):
                    folders.append(folder)

        walk = os.walk(self.root, True, self._error)

        files = {}

        for dir_path, dir_names, file_names in walk:
            for file_name in file_names:
                file_path = os.path.join(dir_path, file_name)

                if not FolderMetadata._folder_excluded(self, dir_path[len(self.root):]):
                    file_metadata = FileMetadata(self.root, file_path)
                    files[file_metadata.path] = file_metadata

        return set(folders), files

    # Return true iff a folder is in the exclusions list, or if a folder in the exclusions list contains that folder
    def _folder_excluded(self, folder):
        matches = [exclusion for exclusion in self.exclusions
                   if folder == exclusion or folder.startswith(exclusion + os.path.sep)]

        return len(matches) > 0

    def _error(self, exception):
        raise AppException(f'FileMetadata Error: root: "{self.root}" exception: {exception}', exception)
