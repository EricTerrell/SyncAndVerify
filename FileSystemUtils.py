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
import stat
import win32file
import win32api
import win32con
import pywintypes
import shutil
import platform
from tenacity import *
from StringLiterals import StringLiterals
from AppException import AppException
from Constants import Constants
from Globals import app_globals


def copy_file_before_callback(retry_state):
    if retry_state.attempt_number > 1:
        app_globals.log.print(f'***** FileSystemUtils.copy_file: attempt_number: {retry_state.attempt_number} file path: {retry_state.args[1]}')


class FileSystemUtils:
    @staticmethod
    def canonical_folder_path(path):
        return os.path.abspath(path) + os.sep

    # https://stackoverflow.com/questions/4996405/how-do-i-change-the-file-creation-date-of-a-windows-file
    @staticmethod
    def get_file_date_times(file_path):
        return (os.path.getctime(file_path),
                os.path.getmtime(file_path),
                os.path.getatime(file_path))

    @staticmethod
    # TODO: WARNING! call to CreateFile can hang. Only used in unit tests currently.
    def set_file_date_times(file_path, creation_time, last_modification_time, last_access_time):
        if platform.system() == StringLiterals.PLATFORM_WINDOWS:
            creation_time = pywintypes.Time(int(creation_time))
            last_modification_time = pywintypes.Time(int(last_modification_time))
            last_access_time = pywintypes.Time(int(last_access_time))

            windows_file_handle = None

            try:
                windows_file_handle = win32file.CreateFile(file_path, win32con.GENERIC_WRITE,
                                                           win32con.FILE_SHARE_READ |
                                                           win32con.FILE_SHARE_WRITE |
                                                           win32con.FILE_SHARE_DELETE,
                                                           None,
                                                           win32con.OPEN_EXISTING,
                                                           win32con.FILE_ATTRIBUTE_NORMAL,
                                                           None)

                win32file.SetFileTime(windows_file_handle, creation_time, last_access_time, last_modification_time)

            finally:
                if windows_file_handle is not None:
                    windows_file_handle.close()

    @staticmethod
    @retry(wait=wait_fixed(Constants.RETRY_WAIT), stop=stop_after_attempt(Constants.MAX_RETRIES),
           before=copy_file_before_callback)
    def copy_file(source_file_path, destination_file_path):
        if os.path.exists(destination_file_path):
            try:
                os.remove(destination_file_path)
            except PermissionError:
                os.chmod(destination_file_path, stat.S_IWRITE)
                os.remove(destination_file_path)

        shutil.copy2(source_file_path, destination_file_path)

    @staticmethod
    def label_to_drive_letter(volume_label):
        for letter in FileSystemUtils._char_range('A', 'Z'):
            try:
                volume_info = win32api.GetVolumeInformation(f'{letter}:\\')

                if volume_info[0] == volume_label:
                    return letter

            except pywintypes.error:
                pass

        raise AppException(f'Cannot map volume label "{volume_label}" to drive letter')

    @staticmethod
    def _char_range(c1, c2):
        # https://stackoverflow.com/questions/7001144/range-over-character-in-python
        """Generates the characters from `c1` to `c2`, inclusive."""
        """Using range instead of xrange as xrange is deprecated in Python3"""
        for c in range(ord(c1), ord(c2) + 1):
            yield chr(c)
