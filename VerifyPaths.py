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
from AppException import AppException


class VerifyPaths:
    @staticmethod
    def verify(source_path, destination_path, require_destination_path=False):
        source_path = os.path.abspath(source_path)
        destination_path = os.path.abspath(destination_path)

        if not os.path.exists(source_path):
            raise AppException(f'Source path does not exist: "{source_path}"')

        if require_destination_path and not os.path.exists(destination_path):
            raise AppException(f'Destination path does not exist: "{destination_path}"')

        if source_path == destination_path:
            raise AppException(f'Source path and destination path must be different: "{source_path}"')

        return source_path, destination_path

