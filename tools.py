#!/usr/bin/env python3
"""Setup basic configuration and tools accessible to other AutoInk modules.

**Author: Jonathan Delgado**

"""
#------------- Imports -------------#
import sublime
import subprocess
from pathlib import Path
import os # sorting svg files
import shutil # checking that Inkscape is installed
#--- Custom imports ---#
#------------- Fields -------------#
__version__ = '0.2.1'
EDITOR = 'inkscape'
FILE_EXT = '.svg'
#======================== Settings & Editor ========================#

def editor_is_installed():
    """ Checks that Inkscape is installed. """
    return shutil.which(EDITOR) is not None


def load_settings():
    """ Loads and parses any necessary settings. """
    subl_settings = sublime.load_settings("AutoInk.sublime-settings")
    settings = subl_settings.to_dict()

    # Make sense of "~" if provided
    settings['templates'] = Path(settings['templates']).expanduser()
    # Convert the figure command into a single string since it's a list in file
    settings['command'] = '\n'.join(subl_settings['latex_command'])

    return settings


def launch_editor(path):
    """ Launches the figure editing program for file at path. """
    if not editor_is_installed():
        print(f'No {EDITOR} installation found. Cannot launch editor.')
        return

    subprocess.Popen([EDITOR, path])


def get_svgs_in_folder(folder, sort=None):
    """ Gets the svg files in the folder provided. """
    files = list(folder.glob('*' + FILE_EXT))

    if sort == 'modified date':
        # sort by date modified
        files = sorted(files, key=os.path.getmtime)[::-1]

    return files