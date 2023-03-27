#!/usr/bin/env python3
"""Handles reading into the editor view, such as reading lines of text in the editor.

**Author: Jonathan Delgado**

"""
#------------- Imports -------------#
from pathlib import Path
#--- Custom imports ---#
# from tools.config import *
#------------- Fields -------------#
#======================== Reading ========================#

def get_line(view):
    """ Gets the region of the full line the cursor is currently at """
    return view.line(view.sel()[0])


def read_line(view):
    """ Gets the full line of text at the current cursor position. """
    return view.substr(get_line(view))


def get_current_folder(view):
    """ Gets the current folder the file being edited is in. """
    return Path(view.file_name()).parent


#======================== Writing ========================#


def replace_current_line(view, edit, text):
    """ Replace current line of text. """
    view.replace(edit, get_line(view), text)