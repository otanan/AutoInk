#!/usr/bin/env python3
"""Sets up alerts for plugin interactivity and alerting user.

**Author: Jonathan Delgado**

"""
#------------- Imports -------------#
import sublime
#--- Custom imports ---#
# from tools.config import *
#------------- Fields -------------#
#======================== Helper ========================#

def popup(view, message):
    """ Simple popup message. """
    view.show_popup(message, flags=sublime.PopupFlags.HIDE_ON_CHARACTER_EVENT)