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
from tenacity import *
from FileSystemUtils import FileSystemUtils
from Config import Config
from DateTimeUtils import DateTimeUtils


def before_callback(retry_state):
    if retry_state.attempt_number > 1:
        print(f'***** FileMetadata: attempt_number: {retry_state.attempt_number} root: "{retry_state.args[1]}" path: "{retry_state.args[2]}" ({DateTimeUtils.format_date_time()}) *****')

class FileMetadata:
    @retry(wait=wait_fixed(Config.RETRY_WAIT), before=before_callback, stop=stop_after_attempt(Config.MAX_RETRIES))
    def __init__(self, root, path):
        self.path = path[len(FileSystemUtils.canonical_folder_path(root)):len(path)]
        self.metadata = os.stat(path)

    def files_are_same(self, other):
        return self.path == other.path and \
               self.metadata.st_size == other.metadata.st_size and \
               abs(self.metadata.st_mtime - other.metadata.st_mtime) <= Config.ACCEPTABLE_TIME_DIFFERENCE
