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
import sys
import time
from FolderQuickCompare import FolderQuickCompare
from FolderCompleteCompare import FolderCompleteCompare
from FolderSync import FolderSync
from PowerManagement import PowerManagement
from Log import Log
from Globals import app_globals
from AppException import AppException
from StringLiterals import StringLiterals
from Constants import Constants
from DateTimeUtils import DateTimeUtils
from datetime import timedelta


def print_usage_and_exit():
    app_globals.log.print('usage: {s (sync)|qc (quick compare)|cc (complete compare)} {source folder} {destination folder} {log root folder} {# threads}')
    sys.exit(Constants.EXIT_FAILURE)


def main():
    start_time = time.perf_counter()

    app_globals.log = Log()

    if len(sys.argv) == 6:
        verb = sys.argv[1].upper()

        if verb not in {'S', 'QC', 'CC'}:
            print_usage_and_exit()

        source_path = sys.argv[2]
        destination_path = sys.argv[3]
        log_root = sys.argv[4]
        threads = int(sys.argv[5])

        if threads < 1:
            raise AppException('# threads must be >= 1')

        app_globals.log.print(f"\nStarting at {DateTimeUtils.format_date_time()} {sys.version}\n")

        if not os.path.exists(log_root):
            os.mkdir(log_root)

        try:
            app_globals.log = Log(log_root)
            PowerManagement.prevent_sleep()
            app_globals.log.print(StringLiterals.EMPTY_STRING)

            if verb == 'QC':
                app_globals.log.print(f'Comparing (quick) "{source_path}" and "{destination_path}" ({threads} threads) ({DateTimeUtils.format_date_time()})')

                comparison = FolderQuickCompare.compare(source_path, destination_path, threads)
                FolderQuickCompare.display_results(comparison)
            elif verb == 'CC':
                app_globals.log.print(f'Comparing (complete) "{source_path}" and "{destination_path}" ({threads} threads) ({DateTimeUtils.format_date_time()})')

                comparison = FolderCompleteCompare.compare(source_path, destination_path, threads)
                FolderCompleteCompare.display_results(comparison)
            elif verb == 'S':
                app_globals.log.print(f'Syncing "{source_path}" to "{destination_path}" ({threads} threads) ({DateTimeUtils.format_date_time()})')

                FolderSync.sync(source_path, destination_path, threads)

        except (AppException, OSError, KeyboardInterrupt, BaseException) as exception:
            if isinstance(exception, KeyboardInterrupt):
                error_message_text = StringLiterals.USER_CANCELLED
            else:
                error_message_text = f'{exception}'

            error_message = f'\n{StringLiterals.ERROR_PREFIX}: {error_message_text}\n'
            app_globals.log.print(error_message)
            sys.exit(Constants.EXIT_FAILURE)

        finally:
            app_globals.log.print(f'\nElapsed Time: {DateTimeUtils.format_timedelta(timedelta(seconds=time.perf_counter() - start_time))}')
            app_globals.log.print(f'\nFinished at {DateTimeUtils.format_date_time()}\n')

            PowerManagement.allow_sleep()
            app_globals.log.close()
            sys.exit()

    else:
        print_usage_and_exit()


# Only run when called from the command line (as opposed to the unit testing framework).
if __name__ == '__main__':
    main()
