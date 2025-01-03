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

import unittest
import sys
from CustomBackup import main


class TestCustomBackup(unittest.TestCase):
    VOLUME_LABEL = 'Archived Backup'

    @unittest.skip('integration test')
    def test_quick_compare(self):
        sys.argv = ['TestCustomBackup.py', 'qc', self.VOLUME_LABEL]

        main()

    @unittest.skip('integration test')
    def test_complete_compare(self):
        sys.argv = ['TestCustomBackup.py', 'cc', self.VOLUME_LABEL]

        main()

    @unittest.skip('integration test')
    def test_sync(self):
        sys.argv = ['TestCustomBackup.py', 's', self.VOLUME_LABEL]

        main()


if __name__ == '__main__':
    unittest.main()
