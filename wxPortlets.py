# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wxPortlets module.
# published under BSD license by Mark Muzenhardt.
#===============================================================================

import wx

from wxApi import Portlets, Images
from misc import FileSystem
from dbApi import SQLdb, Tools as dbTools


class DatabaseLogin(wx.Panel):
    def __init__(self, parent, image_path='', ini_filename='', autosave=False, debug=False):
        wx.Panel.__init__(self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 200,460 ), style = wx.TAB_TRAVERSAL)

        self.image_path = image_path
        self.ini_filename = ini_filename
        self.autosave = autosave
        self.debug = debug
        
        self.database = None        
        self.sizer = wx.FlexGridSizer( 2, 1, 0, 0 )
        self.sizer.AddGrowableCol( 0 )
        self.sizer.AddGrowableRow( 0, 1 )
        
        self.sizer.SetFlexibleDirection( wx.BOTH )
        self.sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.portlet_database = Portlets.Database(parent=self)
        self.portlet_database.Hide()
        self.portlet_login = Portlets.Login(parent=self)
        self.svg = Images.SVG( self, self.image_path )
        
        self.sizer.Add(self.svg, 0, wx.ALL|wx.EXPAND)
        self.sizer.Add(self.portlet_login, 0, wx.ALL|wx.EXPAND)
        
        self.SetSizer(self.sizer)
        self.Layout()
        
        # Populate comboboxes -------------------------------------------------
        odbc_drivers = dbTools.get_odbc_drivers()
        self.portlet_database.combobox_odbc.AppendItems(odbc_drivers)
        
        db_engines_list = SQLdb.get_engines()
        self.portlet_database.combobox_engine.AppendItems(db_engines_list)
        
        # Add bottom panel with buttons ---------------------------------------
        bottom_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.sizer.Add(bottom_panel, 1, wx.ALL|wx.EXPAND)
        
        bottom_sizer = wx.FlexGridSizer( 0, 3, 0, 0 )
        bottom_sizer.AddGrowableCol( 1 )
        bottom_sizer.AddGrowableRow( 0 )

        self.togglebutton_preferences = wx.ToggleButton(bottom_panel, label='Einstellungen')
        self.togglebutton_preferences.Bind(wx.EVT_TOGGLEBUTTON, self.on_togglebutton_preferences_toggled, id=wx.ID_ANY)
        bottom_sizer.Add(self.togglebutton_preferences, 1, wx.ALL|wx.ALIGN_LEFT, 5)
        
        self.button_cancel = wx.Button(bottom_panel, label='Abbruch')
        bottom_sizer.Add(self.button_cancel, 1, wx.ALL|wx.ALIGN_RIGHT, 5)
        
        self.button_ok = wx.Button(bottom_panel, label='Ok')
        bottom_sizer.Add(self.button_ok, 1, wx.ALL|wx.ALIGN_RIGHT, 5)

        bottom_panel.SetSizer(bottom_sizer)
        
        
    def on_togglebutton_preferences_toggled(self, event):
        selection = event.GetSelection()
        
        if selection == 1:
            self.sizer.Replace(self.svg, self.portlet_database)
            self.svg.Hide()
            self.portlet_database.Show()
        else:
            self.sizer.Replace(self.portlet_database, self.svg)
            self.svg.Show()
            self.portlet_database.Hide()
        self.Layout()
        
        
        