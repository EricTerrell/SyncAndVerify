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

from datetime import datetime


class DateTimeUtils:
    @staticmethod
    def format_date_time():
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def format_timedelta(timedelta):
        return str(timedelta)[0:-7]
