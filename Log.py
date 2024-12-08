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

import datetime
import os
import sys
from StringLiterals import StringLiterals


class Log:
    def __init__(self, root=None):
        if root is not None:
            if not os.path.exists(root):
                os.mkdir(root)

            self.path = f"{root}{os.sep}{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log"
            self.file = open(self.path, 'w+', encoding=StringLiterals.UTF_8)
        else:
            self.path = None
            self.file = None

    def print(self, content, standard_output=True, log=True):
        if standard_output:
            print(content)
            sys.stdout.flush()

        if log and self.file is not None:
            try:
                print(content, file=self.file)
            except IOError:
                pass

    def close(self):
        if self.file is not None:
            try:
                self.file.close()
            except IOError:
                pass
