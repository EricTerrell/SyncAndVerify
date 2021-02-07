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

import os
from FileSystemUtils import FileSystemUtils


class FileMetadata:
    """
    Acceptable time difference, in seconds, for a presumably identical file to have in the source and destination
    folders. They may differ slightly due to file system implementation differences.
    """

    ACCEPTABLE_TIME_DIFFERENCE = 60

    def __init__(self, root, path):
        self.path = path[len(FileSystemUtils.canonical_folder_path(root)):len(path)]
        self.metadata = os.stat(path)

    def files_are_same(self, other):
        return self.path == other.path and \
               self.metadata.st_size == other.metadata.st_size and \
               abs(self.metadata.st_mtime - other.metadata.st_mtime) <= self.ACCEPTABLE_TIME_DIFFERENCE
