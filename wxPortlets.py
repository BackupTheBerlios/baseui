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
        
        self.image_path = image_path
        self.ini_filename = ini_filename
        self.autosave = autosave
        self.debug = debug
        
        self.database = None
        
        odbc_drivers = dbTools.get_odbc_drivers()
        self.portlet_database.combobox_odbc.AppendItems(odbc_drivers)
        
        db_engines_list = SQLdb.get_engines()
        self.portlet_database.combobox_engine.AppendItems(db_engines_list)
        
        bottom_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        sizer.Add(bottom_panel, 1, wx.ALL|wx.EXPAND)
        
        bottom_sizer = wx.FlexGridSizer( 0, 3, 0, 0 )
        bottom_sizer.AddGrowableCol( 1 )
        bottom_sizer.AddGrowableRow( 0 )

        self.togglebutton_preferences = wx.ToggleButton(bottom_panel, label='Einstellungen')
        self.togglebutton_preferences.Bind(wx.EVT_BUTTON, self.on_togglebutton_preferences_clicked, id=-1)
        bottom_sizer.Add(self.togglebutton_preferences, 1, wx.ALL|wx.ALIGN_LEFT, 5)
        
        self.button_ok = wx.Button(bottom_panel, label='Ok')
        self.button_ok.Bind(wx.EVT_BUTTON, self.on_button_ok_clicked, id = -1)
        bottom_sizer.Add(self.button_ok, 1, wx.ALL|wx.ALIGN_RIGHT, 5)
        
        self.button_cancel = wx.Button(bottom_panel, label='Abbruch')
        self.button_cancel.Bind(wx.EVT_BUTTON, self.on_button_cancel_clicked, id = -1)
        bottom_sizer.Add(self.button_cancel, 1, wx.ALL|wx.ALIGN_RIGHT, 5)
        
        bottom_panel.SetSizer(bottom_sizer)
        
        svg = Images.SVG( self, self.image_path )
        sizer.Add(svg, 0, wx.ALL|wx.EXPAND)
        
        
    def on_button_ok_clicked(self, event):
        print "Mkee!", event
        self.Destroy()
        
        self.frame_start = window_main(None, APP_NAME)
        self.frame_start.Show()
        
        
    def on_button_cancel_clicked(self, event):
        print "cancel", event
        
        
    def on_togglebutton_preferences_clicked(self, event):
        print "preferences", event    