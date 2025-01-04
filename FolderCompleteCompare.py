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
from Executor import Executor
from collections import namedtuple
from FileHash import FileHash
from VerifyPaths import VerifyPaths
from Globals import app_globals
from AppException import AppException
from FolderMetadata import FolderMetadata


class FolderCompleteCompare:
    @staticmethod
    def compare(source_path, destination_path, exclusions, processes = 1):
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

            executor = Executor.create(processes)

            future_source = executor.submit(FolderCompleteCompare._create_file_hashes, source_metadata, source_path)
            future_destination = executor.submit(FolderCompleteCompare._create_file_hashes, destination_metadata,
                                                 destination_path)

            executor.shutdown(wait=True)

            (source_hashes, destination_hashes) = future_source.result(), future_destination.result()

            # in source only
            files_in_source_folder_only = source_hashes.keys() - destination_hashes.keys()

            # in destination only
            files_in_destination_folder_only = destination_hashes.keys() - source_hashes.keys()

            files_in_both_folders = source_hashes.keys() & destination_hashes.keys()

            # source and destination files have different hashes
            different_files = set()

            identical_files = set()

            # source and/or destination file could not be read to be hashed
            could_not_read_files = set()

            for file in files_in_both_folders:
                source_hash = source_hashes[file]
                destination_hash = destination_hashes[file]

                if source_hash == FileHash.ERROR_MARKER or destination_hash == FileHash.ERROR_MARKER:
                    could_not_read_files.add(file)
                else:
                    if source_hash != destination_hash:
                        different_files.add(file)
                    else:
                        identical_files.add(file)

            differences = len(files_in_source_folder_only) + len(files_in_destination_folder_only) + len(
                could_not_read_files) + len(different_files)

            folders_in_source_folder_only = source_metadata[0] - destination_metadata[0]
            folders_in_destination_folder_only = destination_metadata[0] - source_metadata[0]

            folders_in_both_folders = source_metadata[0] & destination_metadata[0]

            CompleteComparison = namedtuple('CompleteComparison',
                                            ['folders_in_source_folder_only',
                                             'folders_in_destination_folder_only',
                                             'folders_in_both_folders',
                                             'files_in_source_folder_only',
                                             'files_in_destination_folder_only',
                                             'files_in_both_folders',
                                             'identical_files',
                                             'different_files',
                                             'could_not_read_files',
                                             'source_hashes',
                                             'destination_hashes',
                                             'differences'])

            return CompleteComparison(folders_in_source_folder_only,
                                      folders_in_destination_folder_only,
                                      folders_in_both_folders,
                                      files_in_source_folder_only,
                                      files_in_destination_folder_only,
                                      files_in_both_folders,
                                      identical_files,
                                      different_files,
                                      could_not_read_files,
                                      source_hashes,
                                      destination_hashes,
                                      differences)
        except (IOError, OSError, BaseException) as exception:
            raise AppException(f'{exception}', exception)

    @staticmethod
    def _create_file_hashes(metadata, root_path):
        file_hashes = {}

        root_path_string = f'{root_path}'

        file_hash = FileHash()

        for filepath in metadata[1].keys():
            file_full_path = os.path.join(root_path, filepath)
            file_full_path_string = f'{file_full_path}'
            file_short_path = file_full_path_string[len(root_path_string):len(file_full_path_string)]
            file_hashes[file_short_path] = file_hash.create_file_hash(file_full_path)

        return file_hashes

    @staticmethod
    def display_results(comparison):
        if len(comparison.folders_in_source_folder_only) > 0:
            # folders in source only
            app_globals.log.print(f'\tFolders in Source Folder Only: {len(comparison.folders_in_source_folder_only):,}')
            FolderCompleteCompare._print_paths(comparison.folders_in_source_folder_only)

        if len(comparison.folders_in_destination_folder_only) > 0:
            # folders in source only
            app_globals.log.print(f'\tFolders in Destination Folder Only: {len(comparison.folders_in_destination_folder_only):,}')
            FolderCompleteCompare._print_paths(comparison.folders_in_destination_folder_only)

        if len(comparison.files_in_source_folder_only) > 0:
            # files in source only
            app_globals.log.print(f'\tFiles in Source Folder Only: {len(comparison.files_in_source_folder_only):,}')
            FolderCompleteCompare._print_paths(comparison.files_in_source_folder_only)

        if len(comparison.files_in_destination_folder_only) > 0:
            # files in destination only
            app_globals.log.print(f'\n\tFiles in Destination Folder Only: {len(comparison.files_in_destination_folder_only):,}')
            FolderCompleteCompare._print_paths(comparison.files_in_destination_folder_only)

        if len(comparison.files_in_both_folders) != len(comparison.identical_files) or \
                len(comparison.different_files) > 0 or len(comparison.could_not_read_files) > 0:
            # in both source and destination
            app_globals.log.print(
                f'\n\tFiles in Source and Destination Folders: {len(comparison.files_in_both_folders):,} Identical: {len(comparison.identical_files):,} Different: {len(comparison.different_files):,} Read Errors: {len(comparison.could_not_read_files):,}')

        for file in comparison.different_files:
            source_hash = comparison.source_hashes[file]
            destination_hash = comparison.destination_hashes[file]

            if source_hash != destination_hash:
                app_globals.log.print(f'\tFILES ARE DIFFERENT: file: "{file}" source hash: "{source_hash}" destination hash: "{destination_hash}"')

        for file in comparison.could_not_read_files:
            source_hash = comparison.source_hashes[file]
            destination_hash = comparison.destination_hashes[file]

            if source_hash != destination_hash:
                app_globals.log.print(f'\tCOULD NOT READ FILE(S): file: "{file}" source hash: "{source_hash}" destination hash: "{destination_hash}"')

        app_globals.log.print(f'\tDifferences (complete compare): {comparison.differences}')

    @staticmethod
    def _print_paths(path_set):
        for path in path_set:
            app_globals.log.print(f'\t\t"{path}"')
