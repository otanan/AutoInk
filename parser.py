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
    # remove punctuation
    text = text.replace('.', '').replace("'", '')

    # Remove line breaks and whitespace
    text = text.strip().replace(' ', delim)

    # lowercase
    text = text.lower()

    return text


def text_to_name(line):
    """ Convert the line of text to a properly formatted name. """
    return line.strip()


def name_to_caption(figure_name):
    """ Convert the figure name to a usable caption. """
    return str(figure_name).strip().capitalize() + '.'


def format_latex_command(command, fig_name, label):
    # The raw line will be used to caption the figure.
    caption = name_to_caption(fig_name)
    fname = str_to_fname(fig_name)
    return command.format(
        AI_file_name=f'{{{fname}}}',
        # Caption the figure with the raw line adjusted
        AI_caption=f'{{{caption}}}',
        # Label the figure with the same name as the file
        AI_fig_name=f'{{fig:{fig_name}}}',
    )