#!/usr/bin/env python3
"""Handles reading and writing in the editor view, such as reading lines of text in the editor.

**Author: Jonathan Delgado**

"""
#------------- Imports -------------#
from pathlib import Path
import sublime_plugin
#--- Custom imports ---#
#------------- Fields -------------#
#======================== Reading ========================#

def in_tex_file(view):
    """ Returns True if the current view is a tex file. """
    return view.match_selector(0, 'text.tex.latex')


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

def replace_current_line(view, text):
    """ Replace current line of text. """
    view.run_command( 'replace_current_line', {'text': text} )


class ReplaceCurrentLineCommand(sublime_plugin.TextCommand):
    def run(self, edit, text):
        view = self.view
        view.replace(edit, get_line(view), text)