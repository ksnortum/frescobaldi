"""

This small script creates a POT file ('frescobaldi.pot') for the translations
by extracting all messages from Python source files.

It also creates a POT file ('userguide.pot') for the translation of all
paragraphs of the user guide.

The userguide.pot does not contain translatable strings that also appear in
frescobaldi.pot.

"""

import argparse
import glob
import os
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument("language", help="language to update")
language = parser.parse_args().language

frescobaldi_src = "frescobaldi/"
sys.path[0:0] = [frescobaldi_src, "i18n/"]

import appinfo
import md2pot

# 1. create a POT file for the messages, harvested from the source code
command = [
    'xgettext',
    '-D', 'i18n/frescobaldi',
    '-o', 'frescobaldi.pot',
    f'--package-name={appinfo.name}',
    f'--package-version={appinfo.version}',
    f'--msgid-bugs-address={appinfo.maintainer_email}',
    '--add-comments=L10N',
    # Empty the default keyword list
    '--keyword',
    # Custom keywords for python files.
    '--keyword=_:1c,2,3,4t',    # context, message, plural, count
    '--keyword=_:1,2,3t',       # message, plural, count
    '--keyword=_:1c,2,2t',      # context, message
    '--keyword=_:1,1t',         # message
    # Default keywords for .desktop file
    '--keyword=Name',
    '--keyword=GenericName',
    '--keyword=Comment',
    '--keyword=Icon',
    '--keyword=Keywords',
]

for root, dirs, files in sorted(os.walk(frescobaldi_src)):
    for f in sorted(files):
        if f.endswith('.py') and f[0] != '.':
            command.append(os.path.join("../../", root, f))
command.append('../../i18n/messages.py')   # dummy messages file with some Qt i18n strings
command.extend(['../../linux/org.frescobaldi.Frescobaldi.desktop.in', '../../linux/org.frescobaldi.Frescobaldi.metainfo.xml.in'])
result = subprocess.call(command)

# 2. create a POT file for the user guide
userguide = sorted(glob.glob(os.path.join(frescobaldi_src, 'userguide', '*.md')))
md2pot.md2pot('temp.pot', userguide)
subprocess.call('msguniq -t UTF-8 -o userguide.pot temp.pot'.split())
os.remove("temp.pot")

# 3. Update PO files
frescobaldi_po = f"i18n/frescobaldi/{language}.po"
userguide_po = f"i18n/userguide/{language}.po"
subprocess.run(["msgmerge", "-U", frescobaldi_po, "frescobaldi.pot"])
subprocess.run(["msgmerge", "-U", userguide_po, "userguide.pot"])

# 4. Remove obsolete messages (we don't want them, they clutter the files)
subprocess.run(["msgattrib", "--no-obsolete", "-o", frescobaldi_po, frescobaldi_po])
subprocess.run(["msgattrib", "--no-obsolete", "-o", userguide_po, userguide_po])

# 5. Clean up
os.remove("frescobaldi.pot")
os.remove("userguide.pot")
