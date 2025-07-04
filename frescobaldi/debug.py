# This module helps with debugging Frescobaldi.
#
# Start a Python shell
# Enter: from frescobaldi.debug import *
# This runs Frescobaldi, installs some nice __repr__() methods, connects some
# signals to debug-print functions, and imports the most important modules such
# as app.



import sys

from frescobaldi.__main__ import main

from . import toplevel
toplevel.install()

import app
import document


def doc_repr(self):
    index = app.documents.index(self)
    return f'<Document #{index} "{self.url().toString()}">'
document.Document.__repr__ = doc_repr

@app.documentCreated.connect
def f(doc):
    print("created:", doc)

@app.documentLoaded.connect
def f(doc):
    print("loaded:", doc)

@app.documentClosed.connect
def f(doc):
    print("closed:", doc)

@app.jobStarted.connect
def f(doc, job):
    print('job started:', doc)
    print(job.command)

@app.jobFinished.connect
def f(doc, job, success):
    print('job finished', doc)
    print('success:', success)


# more to add...


# delete unneeded stuff
del f, doc_repr

def modules():
    """Print the list of loaded modules."""
    print('\n'.join(v.__name__ for k, v in sorted(sys.modules.items()) if v is not None))


# avoid builtins._ being overwritten
sys.displayhook = app.displayhook

# instantiate app and create a mainwindow, etc
main(debug=True)

# be friendly and import Qt stuff
# suppress ruff F403 lint check
from PyQt6.QtCore import *  # noqa: F403
from PyQt6.QtGui import *  # noqa: F403
