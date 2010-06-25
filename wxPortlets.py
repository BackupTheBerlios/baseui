# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wxPortlets module.
# published under BSD license by Mark Muzenhardt.
#===============================================================================

import wx


from misc import FileSystem, Windows
from dbApi import SQLdb


class DatabaseLogin(object):
    def __init__(self, ini_filename='', autosave=False, parent=None, debug=False):
        self.ini_filename = ini_filename
        self.autosave = autosave
        self.debug = debug
        self.database = None
        
        print Windows.get_odbc_from_winreg()
        