"""
  SyncAndVerify
  (C) Copyright 2024, Eric Bergman-Terrell

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

import unittest
from BaseTest import BaseTest
from VerifyPaths import VerifyPaths
from AppException import AppException


class TestVerifyPaths(BaseTest):
    def test_invalid_source_path(self):
        valid_path = self.get_temp_folder()
        invalid_path = 'c:\\temp\\thisfolderdoesnotexist'

        with self.assertRaises(AppException):
            VerifyPaths.verify(invalid_path, valid_path)

    def test_equal_paths(self):
        valid_path = self.get_temp_folder()

        with self.assertRaises(AppException):
            VerifyPaths.verify(valid_path, valid_path)


if __name__ == '__main__':
    unittest.main()
