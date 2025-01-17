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
import sys
import time
import traceback

from FolderQuickCompare import FolderQuickCompare
from FolderCompleteCompare import FolderCompleteCompare
from FolderSync import FolderSync
from Log import Log
from Globals import app_globals
from AppException import AppException
from StringLiterals import StringLiterals
from Constants import Constants
from PowerManagement import PowerManagement
from DateTimeUtils import DateTimeUtils
from datetime import timedelta


def print_usage_and_exit():
    app_globals.log.print('usage: {s (sync)|qc (quick compare)|cc (complete compare)} {source folder} {destination folder} {log root folder} {# processes or threads (1 or 2)}')
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
        processes = int(sys.argv[5])
        exclusions = []

        if processes < 1 or processes > 2:
            raise AppException('# processes must be 1 or 2')

        app_globals.log.print(f"\nStarting at {DateTimeUtils.format_date_time()} {sys.version}\n")

        if not os.path.exists(log_root):
            os.mkdir(log_root)

        try:
            app_globals.log = Log(log_root)
            PowerManagement.prevent_sleep()
            app_globals.log.print(StringLiterals.EMPTY_STRING)

            if verb == 'QC':
                app_globals.log.print(f'Comparing (quick) "{source_path}" and "{destination_path}" exclusions: "{exclusions}" ({processes} processes) ({DateTimeUtils.format_date_time()})')

                comparison = FolderQuickCompare.compare(source_path, destination_path, exclusions, processes)
                FolderQuickCompare.display_results(comparison)
            elif verb == 'CC':
                app_globals.log.print(f'Comparing (complete) "{source_path}" and "{destination_path}" exclusions: "{exclusions}" ({processes} processes) ({DateTimeUtils.format_date_time()})')

                comparison = FolderCompleteCompare.compare(source_path, destination_path, exclusions, processes)
                FolderCompleteCompare.display_results(comparison)
            elif verb == 'S':
                app_globals.log.print(f'Syncing "{source_path}" to "{destination_path}" exclusions: "{exclusions}" ({processes} processes) ({DateTimeUtils.format_date_time()})')

                FolderSync.sync(source_path, destination_path, exclusions, processes)

        except (AppException, OSError, KeyboardInterrupt, BaseException, ZeroDivisionError) as exception:
            if isinstance(exception, KeyboardInterrupt):
                error_message_text = StringLiterals.USER_CANCELLED
            else:
                error_message_text = f'{exception.__class__.__name__}\n\targs: {exception.args}\n\tcause: {exception.__cause__}\n\tcontext: {exception.__context__}\n\ttraceback: {traceback.format_exc()}'

            if isinstance(exception, ZeroDivisionError):
                app_globals.log.print(traceback.format_exc())

            error_message = f'\n{StringLiterals.ERROR_PREFIX}: {error_message_text}\n'
            app_globals.log.print(error_message)
            sys.exit(Constants.EXIT_FAILURE)

        finally:
            app_globals.log.print(f'\nElapsed Time: {timedelta(seconds=time.perf_counter() - start_time)}')
            app_globals.log.print(f'\nFinished at {DateTimeUtils.format_date_time()}\n')

            PowerManagement.allow_sleep()
            app_globals.log.close()
            sys.exit()

    else:
        print_usage_and_exit()


# Only run when called from the command line (as opposed to the unit testing framework).
if __name__ == '__main__':
    main()
