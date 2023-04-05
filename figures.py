#!/usr/bin/env python3
"""Logic related to finding a figures folder and creating new figures.

**Author: Jonathan Delgado**

"""
#------------- Imports -------------#
from pathlib import Path
import shutil # copying the template
#--- Custom imports ---#
from .tools import launch_editor
from . import viewer
#------------- Fields -------------#
#======================== Folder searching ========================#


def find_folder(view, depth=2, possible_names=['figures'], make_ok=False):
    """ Finds the folder designated for storing figures.
        
        Args:
            view (sublime.view): the sublime view of the current project.
    
        Kwargs:
            depth (int): the maximum number of parent folders to check.

            possible_names (list): the possible names the figures folder would have.

            make_ok (Bool): whether to make a figures folder if none could be found.
    
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
    if not make_ok:
        return None

    print('No figures folder found. Creating one...')
    return _make_folder(view, name=possible_names[0])


def _make_folder(view, name='figures'):
    """ Makes the figures folder in the case where None was found. """
    # Call it the top ranked folder
    figures_folder = viewer.get_current_folder(view) / name
    figures_folder.mkdir()
    return figures_folder


#======================== LaTeX ========================#

def insert_command_and_copy_template(
        view, command, template_path, target_path
    ):
    """ Inserts the latex command at the cursor, copies the template and opens the editor. """
        # Copy the template directly
    viewer.replace_current_line(view, command)
    _create_figure(template_path, target_path)



def _create_figure(template_path, target_path):
    """ Create the actual .svg file or copy from an existing template. """
    # Search the figures path to find existing figures with same name
    if not target_path.is_file():
        # print('No figures found, copying template.')
        # If no, copy figure template to figure folder with correct name
        shutil.copy2(template_path, target_path)
        # Launches the app with the copied figure file for editing
        launch_editor(target_path)

    print('Finished.')