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

import hashlib
from tenacity import *
from Globals import app_globals
from Constants import Constants


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

                while True:
                    file_bytes = file.read(self.BLOCK_SIZE)

                    if len(file_bytes) == 0:
                        return hash_algorithm.hexdigest()

                    hash_algorithm.update(file_bytes)

        except OSError as os_error:
            app_globals.log.print(
                f'***** FileHash.create_file_hash OSError cannot read file: {path} error: {os_error} *****')
            app_globals.log.print(f'\terrorno: {os_error.errno} winerror: {os_error.winerror} strerror: {os_error.strerror} filename: {os_error.filename}')

            raise

    @staticmethod
    def _get_hash_algorithm():
        return hashlib.sha256()

