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

import ctypes
import platform
from Globals import app_globals
from StringLiterals import StringLiterals


class PowerManagement:
    # https://trialstravails.blogspot.com/2017/03/preventing-windows-os-from-sleeping.html

    _ES_CONTINUOUS = 0x80000000
    _ES_SYSTEM_REQUIRED = 0x00000001

    @staticmethod
    def prevent_sleep():
        if platform.system() == StringLiterals.PLATFORM_WINDOWS:
            app_globals.log.print("Preventing Windows from going to sleep")
            ctypes.windll.kernel32.SetThreadExecutionState(
                PowerManagement._ES_CONTINUOUS | PowerManagement._ES_SYSTEM_REQUIRED)

    @staticmethod
    def allow_sleep():
        if platform.system() == StringLiterals.PLATFORM_WINDOWS:
            app_globals.log.print("Allowing Windows to go to sleep")
            ctypes.windll.kernel32.SetThreadExecutionState(PowerManagement._ES_CONTINUOUS)
