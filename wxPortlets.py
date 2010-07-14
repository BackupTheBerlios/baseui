# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wxPortlets module.
# published under BSD license by Mark Muzenhardt.
#===============================================================================

import wx

from wxApi import Portlets
from misc import FileSystem
from dbApi import SQLdb, Tools as dbTools


class DatabaseLogin(wx.Panel):
    def __init__(self, parent, ini_filename='', autosave=False, debug=False):
        wx.Panel.__init__(self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 200,460 ), style = wx.TAB_TRAVERSAL)

        sizer = wx.FlexGridSizer( 2, 1, 0, 0 )
        sizer.AddGrowableCol( 0 )
        sizer.AddGrowableRow( 0, 1 )
        
        sizer.SetFlexibleDirection( wx.BOTH )
        sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.portlet_database = Portlets.Database(parent=self)
        self.portlet_login = Portlets.Login(parent=self)
        
        sizer.Add(self.portlet_database, 0, wx.ALL|wx.EXPAND)
        sizer.Add(self.portlet_login, 0, wx.ALL|wx.EXPAND)
        
        self.SetSizer(sizer)
        self.Layout()
        
        self.ini_filename = ini_filename
        self.autosave = autosave
        self.debug = debug
        self.database = None
        
        odbc_drivers = dbTools.get_odbc_drivers()
        self.portlet_database.combobox_odbc.AppendItems(odbc_drivers)
        
        db_engines_list = SQLdb.get_engines()
        self.portlet_database.combobox_engine.AppendItems(db_engines_list)
        
        
        
        