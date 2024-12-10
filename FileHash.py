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

import hashlib
import os
from tenacity import *
from Globals import app_globals
from Constants import Constants
from AppException import AppException


def before_callback(retry_state):
    if retry_state.attempt_number > 1:
        app_globals.log.print(f'***** FileHash.create_file_hash: attempt_number: {retry_state.attempt_number} file path: {retry_state.args[1]}')


ERROR_MARKER = '<<ERROR>>'


def return_error_marker(retry_state):
    app_globals.log.print(
        f'***** FileHash.create_file_hash: failing after retries. attempt_number: {retry_state.attempt_number} File path: {retry_state.args[1]}')
    return ERROR_MARKER


class FileHash:
    BLOCK_SIZE = 65536

    @retry(wait=wait_fixed(Constants.RETRY_WAIT), stop=stop_after_attempt(Constants.MAX_RETRIES),
           before=before_callback, retry_error_callback=return_error_marker)
    def create_file_hash(self, path):
        try:
            with open(path, 'rb') as file:
                hash_algorithm = FileHash._get_hash_algorithm()
                hash_algorithm_characters = hash_algorithm.digest_size * 2

                while True:
                    file_bytes = file.read(self.BLOCK_SIZE)

                    if len(file_bytes) == 0:
                        result = hash_algorithm.hexdigest()

                        # Paranoia code
                        if len(result) != hash_algorithm_characters or len(result) == 0 or \
                                len(result.strip()) != hash_algorithm_characters:
                            raise AppException(f'Incorrect hash length: {len(result)} hash: "{result}" hash_algorithm_characters: {hash_algorithm_characters}')

                        return result

                    hash_algorithm.update(file_bytes)

        except OSError as os_error:
            app_globals.log.print(
                f'***** FileHash.create_file_hash OSError cannot read file: {path} error: {os_error} *****')
            app_globals.log.print(f'\terrorno: {os_error.errno} winerror: {os_error.winerror} strerror: {os_error.strerror} filename: {os_error.filename}')

            raise

    @staticmethod
    # Return a folder path that matches the format of folder paths in the exclusions list
    def _get_check_folder_path(path, root_path):
        check_folder = path[len(root_path) + 1:]
        sep_pos = check_folder.find(os.path.sep)

        if sep_pos != -1:
            check_folder = check_folder[:sep_pos]

        return check_folder

    @staticmethod
    def _get_hash_algorithm():
        return hashlib.sha256()

