#!/usr/bin/env python3
"""Runs command to easily import new Inkscape figures in LaTeX or import existing ones.

Provides hotkey support to generate Inkscape figures from existing templates. Inspired by https://castel.dev/post/lecture-notes-2/.

**Author: Jonathan Delgado**

"""
#------------- Imports -------------#
import sublime, sublime_plugin
import pathlib
from pathlib import Path
import shutil
# File searching
import glob
# Running Bash commands
import subprocess
#------------- Fields -------------#
__version__ = '0.0.0.2'
#======================== Settings ========================#
_F_EXT = '.svg'
_PROGRAM_NAME = 'inkscape'

template_path = (Path(__file__).parent / 'template').with_suffix(_F_EXT)

#======================== Helper ========================#

def is_valid_line(line):
    """ Check whether the line read from the view is a valid line for a figure name. """
    return line.strip() != ''


def line_to_fname(line, delim='_'):
    """ Converts an arbitrary line of text to a usable filename. """
    # Remove white-space
    return line.strip().replace(' ', delim).lower()


def line_to_name(line):
    """ Convert the line of text to a properly formatted name. """
    return line.strip()


def load_settings():
    """ Loads and parses any necessary settings. """
    subl_settings = sublime.load_settings("AutoInk.sublime-settings")
    settings = subl_settings.to_dict()

    # Sublime injects the home for paths
    settings['templates'] = Path.home() / settings['templates'].replace('~/', '')
    # Convert the figure command into a single string since it's a list in file
    settings['command'] = '\n'.join(subl_settings['latex_command'])

    return settings


def name_to_caption(figure_name):
    """ Convert the figure name to a usable caption. """
    return figure_name.strip().capitalize() + '.'


def find_figures_folder(view, depth=2, possible_names=['figures']):
    """ Finds the folder designated for storing figures.
        
        Args:
            view (sublime.view): the sublime view of the current project.
    
        Kwargs:
            depth (int): the maximum number of parent folders to check.

            possible_names (list): the possible names the figures folder would have.
    
        Returns:
            (pathlib.PosixPath/None): the path to the figures folder, or None if none was found.
    
    """
    current_folder = get_current_folder(view)

    for _ in range(depth):
        # Run through each parent folder to search for figures folder
        for fig_folder_name in possible_names:
            # Go through possible folder names
            path = Path(current_folder) / fig_folder_name

            if path.is_dir():
                # Found the figures folder
                return path

        # None found here, move to parent
        current_folder /= '..'

    # No folder could be found.
    return None


def format_latex_command(command, fig_name, label):
    # The raw line will be used to caption the figure.
    caption = name_to_caption(fig_name)
    return command.format(
        AI_file_name=f'{{{fig_name}}}',
        # Caption the figure with the raw line adjusted
        AI_caption=f'{{{caption}}}',
        # Label the figure with the same name as the file
        AI_fig_name=f'{{fig:{fig_name}}}',
    )


def fname_to_latex_command(fname):
    if isinstance(fname, pathlib.PosixPath):
        # Pull out the filename from the path itself
        fname = fname.stem

    # Naively convert dashes to spaces
    caption = fname.replace('-', ' ')

    return latex_command.format(
        file_name=f'{{{fname}}}',
        # Caption the figure with the raw line adjusted
        caption=f'{{{caption}}}',
        # Label the figure with the same name as the file
        fig_name=f'{{fig:{fname}}}',
    )


def launch_editor(fname):
    """ Launches the figure editing program for fname. """
    subprocess.Popen([_PROGRAM_NAME, fname])


#======================== View reading ========================#


def get_line(view):
    """ Gets the region of the full line the cursor is currently at """
    return view.line(view.sel()[0])


def read_line(view):
    """ Gets the full line of text at the current cursor position. """
    return view.substr(get_line(view))


def get_current_folder(view):
    """ Gets the current folder the file being edited is in. """
    # return os.path.abspath(str(view.file_name()) + '/../')
    return Path(view.file_name()).parent


#======================== View Writing ========================#


def make_figure_folder(view, name='figures'):
    """ Makes the figures folder in the case where None was found. """
    # Call it the top ranked folder
    figures_folder = get_current_folder(view) / name
    figures_folder.mkdir()
    return figures_folder


def replace_current_line(view, edit, text):
    """ Replace current line of text. """
    view.replace(edit, get_line(view), text)


def create_figure(figures_folder, fig_fname, template_path):
    """ Create the actual .svg file or copy from an existing template. """
    template_path = template_path / 'autoink_default.svg'

    # Search the figures path to find existing figures with same name
    files = list(figures_folder.glob(f'{fig_fname}{_F_EXT}'))

    if len(files) == 0:
        print('No figures found, copying template.')
        # If no, copy figure template to figure folder with correct name
        fname = (figures_folder / fig_fname).with_suffix(_F_EXT)
        shutil.copy2(template_path, fname)
        # Launches the app with the copied figure file for editing
        launch_editor(fname)

    print('Finished.')


#======================== Commands ========================#

class NewAutoInkCommand(sublime_plugin.TextCommand):
    """ Reads the text line to generate the figure environment and setup the Inkscape session. """

    def run(self, edit):
        print('Running Figure Command...\n')
        view = self.view

        #--- Get the figure parameters from the line ---#
        # Get the line to parse out the new figure name
        line = read_line(view)
        if not is_valid_line(line):
            # This is an empty line, don't bother parsing this.
            print("Can't parse empty line for a filename.")
            return

        #------------- Main Logic -------------#
        settings = load_settings()
        # Get the name of the actual figure
        fig_name = line_to_name(line)
        # Get the name that the figure file will have
        fig_fname = line_to_fname(line, delim=settings['fname_delimiter'])

        #--- Getting the figures folder ---#
        # Find the folder to store the figure in
        figures_folder = find_figures_folder(
            view, depth=settings['recursive_check'],
            possible_names=settings['figures_folders']
        )

        # If no folder could be found
        if figures_folder is None:
            print('No figures folder found. Creating one...')
            figures_folder = make_figure_folder(
                # Give it the name of the top-ranked folder
                view, settings['figures_folders'][0]
            )

        #--- Paste the LaTeX command ---#
        command = format_latex_command(
            settings['command'], fig_name, label=fig_fname
        )
        replace_current_line(view, edit, command)

        #--- Make the figure ---#
        create_figure(
            figures_folder, fig_fname,
            template_path=settings['templates']
        )


class EditAutoInkCommand(sublime_plugin.WindowCommand):

    def run(self):
        view = self.window.active_view()

        # Load settings
        settings = sublime.load_settings("AutoInk.sublime-settings")

        possible_fig_folder_names = settings.get('figures_folders')
        
        recursive_check = settings.get('recursive_check')


        figures_folder = find_figures_folder(view, recursive_check, possible_fig_folder_names)
        files = list(figures_folder.glob(f'*{_F_EXT}'))
        fnames = [
            file.stem
            for file in files
        ]
        
        # Show list of possible files
        self.window.show_quick_panel(
            # The options
            fnames,
            # The on done method called
            lambda choice_index: self.on_done(choice_index, files),
            placeholder='Choose the Inkscape file to edit...'
        )


    def on_done(self, choice_index, files):
        if choice_index < 0:
            # Choice index is -1 on cancel.
            return
        
        print( f'Editing Inkscape file: {files[choice_index].stem}' )

        fname = files[choice_index]
        subprocess.Popen([_PROGRAM_NAME, fname])

        # Check the settings to control the clipboard on a selection
        settings = sublime.load_settings("AutoInk.sublime-settings")
        if settings.get('set_clipboard_on_edit', True):
            sublime.set_clipboard(fname_to_latex_command(fname))