#!/usr/bin/env python3
"""Runs command to easily import new Inkscape figures in LaTeX or import existing ones.

Provides hotkey support to generate Inkscape figures from existing templates. Inspired by https://castel.dev/post/lecture-notes-2/.

**Author: Jonathan Delgado**

"""
#------------- Imports -------------#
import sublime, sublime_plugin
import pathlib
from pathlib import Path
import shutil # copying the template
import glob # file searching
import subprocess # running Bash commands
#--- Custom imports ---#
from . import viewer
from . import parser
#------------- Fields -------------#
__version__ = '0.0.0.3'
_F_EXT = '.svg'
_PROGRAM_NAME = 'inkscape'
#======================== Helper ========================#

def load_settings():
    """ Loads and parses any necessary settings. """
    subl_settings = sublime.load_settings("AutoInk.sublime-settings")
    settings = subl_settings.to_dict()

    # Make sense of "~" if provided
    settings['templates'] = Path(settings['templates']).expanduser()
    # Convert the figure command into a single string since it's a list in file
    settings['command'] = '\n'.join(subl_settings['latex_command'])

    return settings


def launch_editor(fname):
    """ Launches the figure editing program for fname. """
    subprocess.Popen([_PROGRAM_NAME, fname])


def name_to_caption(figure_name):
    """ Convert the figure name to a usable caption. """
    return str(figure_name).strip().capitalize() + '.'


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
    current_folder = viewer.get_current_folder(view)

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


def get_files_with_extension_in_folder(folder):
    """ Gets the files with the given extension in the folder provided. """
    return list(folder.glob('*' + _F_EXT))


def get_template(view, template_path):
    """ Gets the path to the template file. If the path provided is file, returns the path as-is. If it's a folder, prompts the user for a template to choose from on each run. """
    def set_choice(choice):
        nonlocal template_path
        template_path = Path(choice)

    def prompt_user_for_template():
        sublime.open_dialog(
            set_choice,
            directory=str(template_path)
        )

    if template_path is None: return None

    if template_path.is_file(): return template_path

    # The provided template path is neither a file nor a folder:
    # so it doesn't exist.
    if not template_path.is_dir():
        print("Template path doesn't exist")
        return None

    prompt_user_for_template()
    
    return template_path


#======================== View Writing ========================#


def make_figure_folder(view, name='figures'):
    """ Makes the figures folder in the case where None was found. """
    # Call it the top ranked folder
    figures_folder = viewer.get_current_folder(view) / name
    figures_folder.mkdir()
    return figures_folder


def create_figure(figures_folder, fig_fname, template_path):
    """ Create the actual .svg file or copy from an existing template. """
    # Search the figures path to find existing figures with same name
    fname = (figures_folder / fig_fname).with_suffix(_F_EXT)
    if not fname.is_file():
        print('No figures found, copying template.')
        # If no, copy figure template to figure folder with correct name
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
        line = viewer.read_line(view)
        if parser.is_invalid_line(line):
            # This is an empty line, don't bother parsing this.
            print("Can't parse empty line for a filename.")
            return

        #------------- Main Logic -------------#
        settings = load_settings()
        # Get the name of the actual figure
        fig_name = parser.text_to_name(line)
        # Get the name that the figure file will have
        fig_fname = parser.str_to_fname(
            line, delim=settings['fname_delimiter']
        )

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

        #--- Prepare the command and template ---#
        command = format_latex_command(
            settings['command'], fig_name, label=fig_fname
        )

        template_fname = get_template(view, settings['templates'])
        # Cancel the operation
        if template_fname is None:
            # path choice was canceled on recursive call (see end of function)
            # return None to cancel this operation
            print('Template choosing canceled.')
            return
        else: template_fname = Path(template_fname)

        #--- Incorporate the command ---#
        viewer.replace_current_line(view, edit, command)

        #--- Make the figure ---#
        create_figure(
            figures_folder, fig_fname,
            template_path=template_fname
        )


class EditAutoInkCommand(sublime_plugin.WindowCommand):

    def run(self):
        view = self.window.active_view()

        #------------- Main logic -------------#
        settings = load_settings()
        
        #--- Getting the figures folder ---#
        figures_folder = find_figures_folder(
            view, depth=settings['recursive_check'],
            possible_names=settings['figures_folders']
        )

        files = get_files_with_extension_in_folder(figures_folder)
        fnames = [ file.stem for file in files ]
        
        # Show list of possible files
        self.window.show_quick_panel(
            # Show options
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
        launch_editor(fname)

        # Check the settings to control the clipboard on a selection
        settings = load_settings()
        command = settings['command']

        if settings.get('set_clipboard_on_edit', True):
            command = format_latex_command(command, fname, label=fname)
            sublime.set_clipboard(command)