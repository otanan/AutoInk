#!/usr/bin/env python3
"""Command which prompts user to choose from a selection of templates.

**Author: Jonathan Delgado**

"""
#------------- Imports -------------#
import sublime_plugin
from pathlib import Path
# import shutil # copying the template
# import glob # file searching
# import subprocess # running Bash commands
#--- Custom imports ---#
from .tools import *
from . import figures
#------------- Fields -------------#
#======================== Main ========================#

def move_default_to_front(templates):
    """ Moves default template to front of list if available. """
    if 'default' in templates:
        templates.remove('default')
        templates.insert(0, 'default')

    return templates


class ChooseFigureTemplateCommand(sublime_plugin.WindowCommand):
    """ Prompt the user to choose a template from the templates folder. """

    def run(self, latex_command, templates_folder, target_path):
        view = self.window.active_view()

        templates_folder = Path(templates_folder)
        target_path = Path(target_path)

        #------------- Main logic -------------#
        # Get templates
        templates = get_svgs_in_folder(templates_folder)
        # Make choices pretty by removing extension
        templates = [ file.stem for file in templates ]
        templates = move_default_to_front(templates)

        # Show list of possible files
        self.window.show_quick_panel(
            # Show options
            templates,
            # The on done method called
            lambda choice_index: self.on_done(
                view, choice_index, templates,
                templates_folder, target_path, latex_command
            ),
            placeholder='Choose the template...'
        )


    def on_done(self, view, choice_index, templates, templates_folder, target_path, latex_command):
        if choice_index < 0:
            # Choice index is -1 on cancel.
            print('Template copying canceled...')
            return
        
        print( f'Copying template: {templates[choice_index]}' )
        template_path = (templates_folder / templates[choice_index]).with_suffix(FILE_EXT)

        figures.insert_command_and_copy_template(
            view,
            latex_command, template_path, target_path
        )

        # Check the settings to control the clipboard on a selection
        settings = load_settings()
        if settings.get('set_clipboard_on_edit', True):
            sublime.set_clipboard(latex_command)