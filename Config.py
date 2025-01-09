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

k = 1024

class Config:
    """
    Acceptable time difference, in seconds, for a presumably identical file to have in the source and destination
    folders. They may differ slightly due to file system implementation differences.
    """

    ACCEPTABLE_TIME_DIFFERENCE = 60

    # File comparison (retrieving files for hashing)
    FILE_BLOCK_SIZE = 256 * k

    # seconds
    RETRY_WAIT = 1

    # Retry for 1 hour
    MAX_RETRIES = 60 * 60

