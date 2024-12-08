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
import os
import tempfile
import shutil
from FileSystemUtils import FileSystemUtils
from Log import Log
from Globals import app_globals


class BaseTest(unittest.TestCase):
    @staticmethod
    def get_resource_root():
        return pathlib.PurePath(pathlib.PurePath(os.path.dirname(os.path.abspath(__file__))).parent, 'test resources')

    @staticmethod
    def get_temp_folder():
        return pathlib.PurePath(tempfile.gettempdir(), 'BackupAndVerifyTests')

    def setUp(self) -> None:
        print(f'setUp: test resources root: {self.get_resource_root()} temp test folder: {self.get_temp_folder()}\n')

        shutil.rmtree(self.get_temp_folder(), True)
        shutil.copytree(self.get_resource_root(), self.get_temp_folder())

        app_globals.log = Log(None)

        # Ensure that all files have the same timestamps

        walk = os.walk(self.get_temp_folder(), True)

        creation_time = 1561637788.179921
        last_modification_time = 1407594820.999999
        last_access_time = 1607854408.621261

        for dir_path, dir_names, file_names in walk:
            for file_name in file_names:
                file_path = os.path.join(dir_path, file_name)

                FileSystemUtils.set_file_date_times(file_path, creation_time, last_modification_time, last_access_time)
