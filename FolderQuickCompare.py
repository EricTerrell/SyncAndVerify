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
from collections import namedtuple
from tenacity import *
from FolderMetadata import FolderMetadata
from Executor import Executor
from VerifyPaths import VerifyPaths
from Globals import app_globals
from AppException import AppException
from DateTimeUtils import DateTimeUtils
from Config import Config

def before_callback(retry_state):
    if retry_state.attempt_number > 1:
        print(f'***** FolderQuickCompare: attempt_number: {retry_state.attempt_number} source: "{retry_state.args[0]}" destination: "{retry_state.args[1]}" ({DateTimeUtils.format_date_time()}) *****')


class FolderQuickCompare:
    @staticmethod
    @retry(wait=wait_fixed(Config.RETRY_WAIT), before=before_callback, stop=stop_after_attempt(Config.MAX_RETRIES))
    def compare(source_path, destination_path, exclusions, processes):
        try:
            source_path, destination_path = VerifyPaths.verify(source_path, destination_path, True)

            executor = Executor.create(processes)

            source_folder_metadata = FolderMetadata(source_path, exclusions)
            destination_folder_metadata = FolderMetadata(destination_path, exclusions)

            future_source_metadata = executor.submit(source_folder_metadata.get_metadata)
            future_destination_metadata = executor.submit(destination_folder_metadata.get_metadata)

            executor.shutdown(wait=True)

            (source_metadata, destination_metadata) = \
                future_source_metadata.result(), future_destination_metadata.result()

            folders_to_create = \
                FolderQuickCompare._filter_redundant_folders_to_create(
                    source_metadata[0] - destination_metadata[0])

            folders_to_delete = FolderQuickCompare._filter_redundant_folders_to_delete(
                destination_metadata[0] - source_metadata[0])

            files_to_copy_new = source_metadata[1].keys() - destination_metadata[1].keys()

            common_file_keys = source_metadata[1].keys() & destination_metadata[1].keys()

            files_to_copy_changed = set()

            for common_file_key in common_file_keys:
                source_file_metadata = source_metadata[1][common_file_key]
                destination_file_metadata = destination_metadata[1][common_file_key]

                if not source_file_metadata.files_are_same(destination_file_metadata):
                    files_to_copy_changed.add(common_file_key)

            files_to_copy = files_to_copy_new | files_to_copy_changed

            files_to_copy_metadata = {}

            for file in files_to_copy:
                files_to_copy_metadata[file] = source_metadata[1][file]

            # Don't delete files that are inside folders that will be deleted.
            files_to_delete = (set(filter(lambda file: not FolderQuickCompare._file_in_folders(file, folders_to_delete),
                                          destination_metadata[1].keys() - source_metadata[1].keys()
                                          )))

            differences = len(folders_to_delete) + len(folders_to_create) + len(files_to_delete) + len(files_to_copy)

            QuickComparison = namedtuple('QuickComparison',
                                         ['folders_to_delete', 'folders_to_create', 'files_to_delete', 'files_to_copy',
                                          'files_to_copy_metadata', 'differences'])

            result = QuickComparison(sorted(folders_to_delete), sorted(folders_to_create),
                                     sorted(files_to_delete), sorted(files_to_copy_metadata.keys()),
                                     files_to_copy_metadata, differences)

            return result
        except (IOError, OSError, BaseException) as exception:
            raise AppException(f'{exception}', exception)

    @staticmethod
    def display_results(comparison):
        if len(comparison.folders_to_delete) > 0:
            app_globals.log.print(f'\tFolders to Delete: ({len(comparison.folders_to_delete):,})')

            for folder in comparison.folders_to_delete:
                app_globals.log.print(f'\t\t"{folder}"')

        if len(comparison.folders_to_create) > 0:
            app_globals.log.print(f'\tFolders to Create: ({len(comparison.folders_to_create):,})')

            for folder in comparison.folders_to_create:
                app_globals.log.print(f'\t\t"{folder}"')

        if len(comparison.files_to_delete) > 0:
            app_globals.log.print(f'\n\tFiles to Delete: ({len(comparison.files_to_delete):,})')

            for file in comparison.files_to_delete:
                app_globals.log.print(f'\t\t"{file}"')

        bytes_to_copy = sum(value.metadata.st_size for value in comparison.files_to_copy_metadata.values())

        if len(comparison.files_to_copy) > 0:
            app_globals.log.print(
                f'\tFiles to Copy: {len(comparison.files_to_copy):,} Bytes to Copy: {bytes_to_copy:,}')

            for file in comparison.files_to_copy:
                app_globals.log.print(f'\t\t"{file}"')

        app_globals.log.print(f'\tDifferences (quick compare): {comparison.differences:,}')

    @staticmethod
    def summary(comparison):
        bytes_to_copy = sum(value.metadata.st_size for value in comparison.files_to_copy_metadata.values())

        return f'Folders to Delete: {len(comparison.folders_to_delete):,} Folders to Create: {len(comparison.folders_to_create):,} Files to Delete: {len(comparison.files_to_delete):,} Files to Copy: {len(comparison.files_to_copy):,} Bytes to Copy: {bytes_to_copy:,} Total Differences: {comparison.differences:,}'

    @staticmethod
    def _file_in_folders(file, folders):
        return any(file.startswith(current_folder + os.path.sep) for current_folder in folders)

    """
    Remove redundant folders from removal list. For example, rather than removing these folders:

    folders\\destination\\destination really\\nested\\folder
    folders\\destination\\destination really
    folders\\destination\\destination really\\nested
    folders\\destination\\unique_subfolder_destination

    We can just remove these:

    folders\\destination\\destination really
    folders\\destination\\unique_subfolder_destination

    This method simply removes all folders that have other folders as a prefix.
    """

    @staticmethod
    def _filter_redundant_folders_to_delete(folders):
        return set(filter(lambda folder: not FolderQuickCompare._other_folder_is_prefix(folder, folders), folders))

    @staticmethod
    def _other_folder_is_prefix(folder, folders):
        return any(folder != current_folder and folder.startswith(current_folder + os.path.sep)
                   for current_folder in folders)

    """
    Remove redundant folders from create list. If there are two folders in the list, and one is nested beneath
    the other one, keep the nested one.
    """

    @staticmethod
    def _filter_redundant_folders_to_create(folders):
        return set(
            filter(lambda folder: not FolderQuickCompare._folder_is_prefix_for_other_folder(folder, folders), folders))

    @staticmethod
    def _folder_is_prefix_for_other_folder(folder, folders):
        return any(folder != current_folder and current_folder.startswith(folder + os.path.sep)
                   for current_folder in folders)
