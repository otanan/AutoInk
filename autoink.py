#!/usr/bin/env python3
"""Runs command to easily import new Inkscape figures in LaTeX or import existing ones.

**Author: Jonathan Delgado**

"""
#------------- Imports -------------#
import sublime, sublime_plugin

from pathlib import Path
import shutil
# File searching
import glob
# Running Bash commands
import subprocess
#------------- End imports -------------#

#------------- Settings -------------#

_F_EXT = '.svg'

template_path = (Path(__file__).parent / 'template').with_suffix(_F_EXT)

default_possible_fig_folder_names = [
    'figures',
    'figs',
    'fig',
    'res',
    'img',
    'plots',
]
# Number of parent folders it will search through before giving up on figures 
    # folder
default_recursive_check = 2

latex_command = """
\\begin{{figure}}
    \\includesvg{file_name}
    \\caption{caption}
    \\label{fig_name}
\\end{{figure}}
"""

######################## Functions ########################


def line_to_fname(line):
    """ Converts an arbitrary line of text to a usable filename. """
    # Remove white-space
    # Replace space for OS friendly dashes
    return line.strip().replace(' ', '-').lower()


def get_line(view):
    """ Gets the region of the full line the cursor is currently at """
    return view.line(view.sel()[0])


def read_line(view):
    """ Gets the full line of text at the current cursor position. """
    return view.substr(get_line(view))


def line_to_caption(line):
    """ Convert the line of text to a usable caption. """
    return line.strip().capitalize() + '.'


def replace_current_line(view, edit, text):
    """ Replace current line of text. """
    view.replace(edit, get_line(view), text)


def get_current_folder(view):
    """ Gets the current folder the file being edited is in. """
    # return os.path.abspath(str(view.file_name()) + '/../')
    return Path(view.file_name()).parent


def find_figures_folder(view, recursive_check, possible_fig_folder_names):
    """ Finds the folder designated for figures.
    
        Returns:
            (str): the path of the figures folder if found.
            (None): None if no figures folder could be found.
    
    """
    current_folder = get_current_folder(view)

    for _ in range(recursive_check):
        # Run through each parent folder to search for figures folder
        for fig_folder_name in possible_fig_folder_names:
            # Go through possible folder names
            path = Path(current_folder) / fig_folder_name

            if path.is_dir():
                # Found the figures folder
                return path

        current_folder /= '..'

    # No folder could be found.
    return None


######################## Main ########################


class NewAutoInkCommand(sublime_plugin.TextCommand):
    """ Takes line to create new Inkscape figure. """

    def run(self, edit):
        print('Running Figure Command...\n')
        view = self.view
        # Load settings
        settings = sublime.load_settings("AutoInk.sublime-settings")

        possible_fig_folder_names = settings.get(
            'figures_folders', default_possible_fig_folder_names
        )
        
        recursive_check = settings.get(
            'recursive_check', default_recursive_check
        )

        # Get the line to parse out the new figure name
        line = read_line(view)
        figure_name = line_to_fname(line)
        # The raw line will be used to caption the figure.
        caption = line_to_caption(line)

        ### Find figures folder ###
        # The absolute path of the current file being edited
        figures_folder = find_figures_folder(view, recursive_check, possible_fig_folder_names)
        # If no folder could be found
        if figures_folder is None:
            print('No figures folder found. Creating one.')
            # Make one
            current_folder = get_current_folder(view)
            # Call it the top ranked folder
            figures_folder = current_folder / possible_fig_folder_names[0]
            figures_folder.mkdir()

        ### Paste the LaTeX command ###
        command = latex_command.format(
            file_name=f'{{{figure_name}}}',
            # Caption the figure with the raw line adjusted
            caption=f'{{{caption}}}',
            # Label the figure with the same name as the file
            fig_name=f'{{fig:{figure_name}}}',
        )
        replace_current_line(view, edit, command)

        # Search the figures path to find existing figures with same name
        files = list(figures_folder.glob(f'{figure_name}{_F_EXT}'))

        if len(files) == 0:
            print('No figures found, copying template.')
            # If no, copy figure template to figure folder with correct name
            fname = (figures_folder / figure_name).with_suffix(_F_EXT)
            shutil.copy(template_path, fname)
            # Launches the app with the copied figure file for editing
            subprocess.Popen(['inkscape', fname])

        print('Finished.')


class EditAutoInkCommand(sublime_plugin.WindowCommand):

    def run(self):
        view = self.window.active_view()

        # Load settings
        settings = sublime.load_settings("AutoInk.sublime-settings")

        possible_fig_folder_names = settings.get(
            'figures_folders', default_possible_fig_folder_names
        )
        
        recursive_check = settings.get(
            'recursive_check', default_recursive_check
        )


        figures_folder = find_figures_folder(view, recursive_check, possible_fig_folder_names)
        files = list(figures_folder.glob(f'*{_F_EXT}'))
        fnames = [
            file.stem
            for file in files
        ]
        
        # Show list of possible files
        self.window.show_quick_panel(
            fnames, lambda choice_index: self.on_done(choice_index, files)
        )

    def on_done(self, choice_index, files):
        path = files[choice_index]
        subprocess.Popen(['inkscape', path])