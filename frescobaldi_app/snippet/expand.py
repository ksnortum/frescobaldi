# This file is part of the Frescobaldi project, http://www.frescobaldi.org/
#
# Copyright (c) 2008 - 2014 by Wilbert Berendsen
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# See http://www.gnu.org/licenses/ for more information.

"""
Expand variables like $DATE, $LILYPOND_VERSION etc. in snippets.
"""


import time

import appinfo
import lilypondinfo


ANCHOR, CURSOR, SELECTION = constants = 1, 2, 3 # just some constants

class Expander:
    """Expands variables.

    The methods return text or other events (currently simply integer constants).

    Each variable is documented in the user guide.
    """
    def __init__(self, cursor):
        self.cursor = cursor

    def DATE(self):
        return time.strftime('%Y-%m-%d')

    def LILYPOND_VERSION(self):
        return lilypondinfo.preferred().versionString()

    def FRESCOBALDI_VERSION(self):
        return appinfo.version

    def URL(self):
        return self.cursor.document().url().toString()

    def FILE_NAME(self):
        return self.cursor.document().url().toLocalFile()

    def DOCUMENT_NAME(self):
        return self.cursor.document().documentName()

    def CURSOR(self):
        return CURSOR

    def ANCHOR(self):
        return ANCHOR

    def SELECTION(self):
        return SELECTION if self.cursor.hasSelection() else CURSOR
