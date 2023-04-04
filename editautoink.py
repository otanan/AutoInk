#!/usr/bin/env python3
"""Command for editing existing Inkscape figures in the project.

**Author: Jonathan Delgado**

"""
#------------- Imports -------------#
import sublime
import sublime_plugin
#--- Custom imports ---#
from .tools import *
from . import figures
from . import parser
#------------- Fields -------------#
#======================== Main ========================#


class EditAutoInkCommand(sublime_plugin.WindowCommand):
    """ Open InkScape to edit existing figures. """

    def run(self):
        view = self.window.active_view()

        #------------- Main logic -------------#
        settings = load_settings()
        
        #--- Getting the figures folder ---#
        figures_folder = figures.find_folder(
            view, depth=settings['recursive_check'],
            possible_names=settings['figures_folders']
        )

        files = get_svgs_in_folder(figures_folder, sort='modified date')
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
        
        path = files[choice_index]
        name = path.stem
        print( f'Editing Inkscape file: {name}' )
        launch_editor(path)

        # Check the settings to control the clipboard on a selection
        settings = load_settings()
        command = settings['command']

        if settings.get('set_clipboard_on_edit', True):
            command = parser.format_latex_command(command, name, label=name)
            sublime.set_clipboard(command)