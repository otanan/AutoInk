#!/usr/bin/env python3
"""String parser for validating lines of text and converting them to filenames.

**Author: Jonathan Delgado**

"""
#------------- Imports -------------#
# import sys
#--- Custom imports ---#
# from tools.config import *
#------------- Fields -------------#
#======================== Functions ========================#

def is_invalid_line(line):
    """ Check whether the line read from the view is a valid line for a figure name. """
    return line.strip() == '' or '/' in line or '{' in line or '}' in line


def str_to_fname(text, delim='_'):
    """ Converts an arbitrary text to a usable filename. """
    # Remove white-space
    return text.strip().replace(' ', delim).lower()


def text_to_name(line):
    """ Convert the line of text to a properly formatted name. """
    return line.strip()