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
import shutil
import time
from datetime import timedelta
from tenacity import RetryError
from FileSystemUtils import FileSystemUtils
from FolderQuickCompare import FolderQuickCompare
from VerifyPaths import VerifyPaths
from StringLiterals import StringLiterals
from Globals import app_globals
from AppException import AppException
from FileHash import FileHash
from Executor import Executor
from DateTimeUtils import DateTimeUtils


class FolderSync:
    @staticmethod
    def sync(source_path, destination_path, exclusions, processes = 1):
        start_time = time.perf_counter()

        source_path, destination_path = VerifyPaths.verify(source_path, destination_path)

        try:
            if not os.path.exists(destination_path):
                os.makedirs(destination_path)

            comparison = FolderQuickCompare.compare(source_path, destination_path, exclusions, processes)
            app_globals.log.print(f'\t{FolderQuickCompare.summary(comparison)}')

            if comparison.differences > 0:
                FolderSync._delete_folders(comparison, destination_path)
                FolderSync._delete_files(comparison, destination_path)
                FolderSync._create_folders(comparison, destination_path)
                FolderSync._copy_files(comparison, source_path, destination_path)

                FolderSync._verify_copied_files(comparison, source_path, destination_path, processes)

                # After backup is complete, re-run quick comparison to verify that everything was completed.
                post_sync_comparison = FolderQuickCompare.compare(source_path, destination_path, exclusions, processes)

                app_globals.log.print('\tSynced')
                app_globals.log.print(f'\tChecking Sync: {FolderQuickCompare.summary(post_sync_comparison)}')

                if post_sync_comparison.differences > 0:
                    error_message = f'{StringLiterals.ERROR_PREFIX}: Source folder is not fully synced'
                    app_globals.log.print(error_message)
                    FolderQuickCompare.display_results(post_sync_comparison)
                    raise AppException(error_message)
            else:
                app_globals.log.print('\tNo Need to Sync')

        except (RetryError, IOError, OSError, BaseException) as exception:
            raise AppException(f'{exception}', exception)

        finally:
            app_globals.log.print(
                f'Elapsed Time: {timedelta(seconds=time.perf_counter() - start_time)}\n')

        return comparison

    @staticmethod
    def _delete_readonly_file(action, path, exc):
        if not os.access(path, os.W_OK):
            os.chmod(path, stat.S_IWRITE)
            action(path)
        else:
            raise

    @staticmethod
    def _delete_folders(comparison, destination_path):
        for folder in comparison.folders_to_delete:
            full_path = os.path.join(destination_path, folder)
            shutil.rmtree(full_path, onerror=FolderSync._delete_readonly_file)

    @staticmethod
    def _delete_files(comparison, destination_path):
        for file in comparison.files_to_delete:
            full_path = os.path.join(destination_path, file)

            try:
                os.remove(full_path)
            except PermissionError:
                os.chmod(full_path, stat.S_IWRITE)
                os.remove(full_path)

    @staticmethod
    def _create_folders(comparison, destination_path):
        for folder in comparison.folders_to_create:
            full_path = os.path.join(destination_path, folder)
            os.makedirs(full_path, exist_ok=False)

    @staticmethod
    def _copy_files(comparison, source_path, destination_path):
        start_time = time.perf_counter()

        files_copied = 0
        bytes_copied = 0
        bytes_to_copy = sum(value.metadata.st_size for value in comparison.files_to_copy_metadata.values())

        app_globals.log.print(f'\tCopying files ({DateTimeUtils.format_date_time()})')

        for file in comparison.files_to_copy:
            file_source_path = os.path.join(source_path, file)
            file_destination_path = os.path.join(destination_path, file)

            app_globals.log.print(f'\t{file_destination_path}', standard_output=False)

            FileSystemUtils.copy_file(file_source_path, file_destination_path)

            files_copied += 1
            bytes_copied += comparison.files_to_copy_metadata[file].metadata.st_size

            if bytes_to_copy != 0:
                bytes_percent = (bytes_copied * 100) / bytes_to_copy
            else:
                bytes_percent = 100.0

            app_globals.log.print('\t\tFiles: ({:,}/{:,} {:.2f}%) Bytes: ({:,}/{:,} {:.2f}%)'.format(
                files_copied,
                len(comparison.files_to_copy_metadata),
                (files_copied * 100) / len(comparison.files_to_copy_metadata),
                bytes_copied,
                bytes_to_copy,
                bytes_percent
            ), standard_output=False)

        app_globals.log.print(
            f'\t\tElapsed Time: {timedelta(seconds=time.perf_counter() - start_time)}')

    @staticmethod
    def _verify_copied_files(comparison, source_path, destination_path, processes):
        start_time = time.perf_counter()

        app_globals.log.print(f'\tVerifying copied files ({processes} processes) ({DateTimeUtils.format_date_time()})')

        executor = Executor.create(processes)

        future_source_file_digests      = executor.submit(FolderSync._compute_file_digests, source_path,
                                                          comparison.files_to_copy)
        future_destination_file_digests = executor.submit(FolderSync._compute_file_digests, destination_path,
                                                          comparison.files_to_copy)

        executor.shutdown(wait=True)

        source_file_digests      = future_source_file_digests.result()
        destination_file_digests = future_destination_file_digests.result()

        errors = 0

        for file in comparison.files_to_copy:
            source_file_digest      = source_file_digests[file]
            destination_file_digest = destination_file_digests[file]

            file_source_path = os.path.join(source_path, file)
            file_destination_path = os.path.join(destination_path, file)

            if source_file_digest == FileHash.ERROR_MARKER:
                errors += 1
                error_message = f'Could not compute hash for source file {file_source_path}'
                app_globals.log.print(error_message)

            if destination_file_digest == FileHash.ERROR_MARKER:
                errors += 1
                error_message = f'\tCould not compute hash for destination file {file_destination_path}'
                app_globals.log.print(error_message)

            if destination_file_digest != source_file_digest:
                errors += 1
                error_message = f'\t*****Hash for "{file_source_path}" ({source_file_digest}) does not match hash for "{file_destination_path}" ({destination_file_digest}) *****'
                app_globals.log.print(error_message)

        try:
            if errors > 0:
                error_message = f'\t*****UNSUCCESSFUL VERIFICATION OF COPIED FILES *****'
                raise AppException(error_message)
            elif errors == 0:
                app_globals.log.print(f'\tSuccessfully verified copied files')
        finally:
            app_globals.log.print(
                f'\t\tElapsed Time: {timedelta(seconds=time.perf_counter() - start_time)}')


    @staticmethod
    def _compute_file_digests(path, files_to_copy):
        digests = dict()

        for file in files_to_copy:
            file_path = os.path.join(path, file)
            digest = FileHash().create_file_hash(file_path)
            digests[file] = digest

        return digests