#!/usr/bin/env python3
"""Setup basic configuration and tools accessible to other AutoInk modules.

**Author: Jonathan Delgado**

"""
#------------- Imports -------------#
import sublime
import subprocess
from pathlib import Path
#--- Custom imports ---#
#------------- Fields -------------#
__version__ = '0.0.0.4'
FILE_EXT = '.svg'
#======================== Settings & Editor ========================#

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
    subprocess.Popen(['inkscape', path])


def get_svgs_in_folder(folder):
    """ Gets the svg files in the folder provided. """
    return list(folder.glob('*' + FILE_EXT))