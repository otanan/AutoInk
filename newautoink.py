#!/usr/bin/env python3
"""Runs command to easily import new Inkscape figures in LaTeX or import existing ones.

Provides hotkey support to generate Inkscape figures from existing templates. Inspired by https://castel.dev/post/lecture-notes-2/.

**Author: Jonathan Delgado**

"""
#------------- Imports -------------#
import sublime # accessing the clipboard
import sublime_plugin
#--- Custom imports ---#
from .tools import *
from . import viewer
from . import parser
from . import figures
from . import alerts
#------------- Fields -------------#
#======================== Main ========================#

def get_figure_parameters(text, fname_delimiter='_'):
    """ Pulls relevant information from the text, such as the name of the figure, the name of the file, etc. """
    # Get the name of the actual figure, i.e. Vector Bundle
    fig_name = parser.text_to_name(text)
    # Get the name that the figure file will have, i.e. vector_bundle
    fig_fname = parser.str_to_fname(
        text, delim=fname_delimiter
    )
    return fig_name, fig_fname


class NewAutoInkCommand(sublime_plugin.TextCommand):
    """ Reads the text line to generate the figure environment and setup the Inkscape session. """

    def run(self, edit):
        # Check whether in valid scope
        view = self.view
        if not viewer.in_tex_file(view):
            print('Ignoring AutoInk command since view is not tex file.')
            return

        print(f'AutoInk activated')

        #--- Get the figure parameters from the line ---#
        # Get the line to parse out the new figure name
        line = viewer.read_line(view)
        if parser.is_invalid_line(view, line):
            # This is an empty line, don't bother parsing this.
            # print("Can't parse empty line for a filename.")
            return

        #------------- Main Logic -------------#
        settings = load_settings()
        fig_name, fig_fname = get_figure_parameters(line, settings['fname_delimiter'])

        #--- Getting the figures folder ---#
        # Find the folder to store the figure in
        figures_folder = figures.find_folder(
            view, depth=settings['recursive_check'],
            possible_names=settings['figures_folders'],
            make_ok=True
        )

        target_path = (figures_folder / fig_fname).with_suffix(FILE_EXT)

        #--- Prepare the command and template ---#
        command = parser.format_latex_command(
            settings['command'], fig_name, label=fig_fname,
            indent=parser.get_indentation(line)
        )

        #--- Prompt the user for the template ---#
        # Gets the path to the template file
        template_path = settings['templates']
        if not template_path.exists():
            alerts.popup(view, 'Cannot find templates, path provided is invalid. Check AutoInk settings.')
            return

        if template_path.is_dir():
            # Prompt the user to choose the template, after the template
            sublime.active_window().run_command('choose_figure_template', {
                "latex_command": command,
                "templates_folder": str(template_path),
                "target_path": str(target_path)
            })
        else:
            figures.insert_command_and_copy_template(
                view, command,
                template_path, target_path
            )