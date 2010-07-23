# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wxPortlets module.
# published under BSD license by Mark Muzenhardt.
#===============================================================================

import wx

from wxApi import Portlets, Dialogs
from dbApi import SQLdb, Tools as dbTools
from misc import FileSystem


class DatabaseLogin(wx.Panel):
    def __init__(self, parent, image_path='', ini_path='', autosave=False, debug=False):
        wx.Panel.__init__(self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 200,460 ), style = wx.TAB_TRAVERSAL)
        self.ErrorDialog = Dialogs.Error(parent=self)
        
        self.image_path = image_path
        self.ini_path = ini_path
        self.autosave = autosave
        self.debug = debug
              
        self.sizer = wx.FlexGridSizer( 2, 1, 0, 0 )
        self.sizer.AddGrowableCol( 0 )
        self.sizer.AddGrowableRow( 0, 1 )
        
        self.sizer.SetFlexibleDirection( wx.BOTH )
        self.sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.portlet_database = Portlets.Database(parent=self, autosave=self.autosave)
        self.portlet_database.Hide()
        self.portlet_login = Portlets.Login(parent=self)
        
        png = wx.Image(self.image_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.logo = wx.StaticBitmap(self, -1, png, (10, 5), (png.GetWidth(), png.GetHeight()))

        self.sizer.Add(self.logo, 0, wx.ALL|wx.EXPAND)
        self.sizer.Add(self.portlet_login, 0, wx.ALL|wx.EXPAND)
        
        self.SetSizer(self.sizer)
        self.Layout()
        
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
        
        # Get the database settings -------------------------------------------
        self.database = None  
        self.ini_file = FileSystem.iniFile(self.ini_path)
        self.config_dic = self.get_settings_from_ini()
        self.populate()
        
        self.portlet_database.on_connect = self.connect
        self.portlet_database.on_disconnect = self.disconnect
                
        
    def on_togglebutton_preferences_toggled(self, event):
        selection = event.GetSelection()
        
        if selection == 1:
            self.sizer.Replace(self.logo, self.portlet_database)
            self.logo.Hide()
            self.portlet_database.Show()
        else:
            self.sizer.Replace(self.portlet_database, self.logo)
            self.logo.Show()
            self.portlet_database.Hide()
        self.Layout()
        
        
    # Actions -----------------------------------------------------------------
    def populate(self):
        # First, populate database_portlet                    
        self.portlet_database.populate({'engines': SQLdb.get_engines(),
                                        'drivers': dbTools.get_odbc_drivers()})
        
        # Then, populate login portlet
        
    
    def get_settings_from_db(self, database):
        self.database = database
        if self.database <> None:
            self.config_dic = database.config
        else:
            self.portlet_database.set_disconnected()
            return

        if self.database.connection <> None:
            self.portlet_database.set_connected()
        else:
            self.portlet_database.set_disconnected()
        return self.config_dic


    def get_settings_from_ini(self):
        try:
            self.config_dic = self.ini_file.dictresult('db')
            return self.config_dic
        except Exception, inst:
            dialog = wx.MessageDialog(self, caption='Fehler', 
                                            message='''\
Die Datenbank Konfigurationsdatei ist fehlerhaft
oder nicht vorhanden.

Soll die Konfigurationsdatei neu erstellt werden?''', 
                                            style=(wx.YES_NO | wx.ICON_EXCLAMATION))
            result = dialog.ShowModal()
            
            if result == wx.ID_YES:
                self.config_dic = self.save_settings_to_ini()
                return self.config_dic
        
        
    def save_settings_to_ini(self):
        self.config_dic = self.portlet_database.get_content()
        ini_text = """\
[db]
engine = %(engine)s
driver = %(driver)s
database = %(database)s
host = %(host)s
user = %(user)s
password = %(password)s

""" % self.config_dic

        self.ini_file.save(ini_text)
        return self.config_dic


    def connect(self):
        try:
            self.config_dic = self.portlet_database.get_content()
            self.database = SQLdb.database(self.config_dic.get('engine'), debug=self.debug)
            self.database.connect(database=self.config_dic.get('database'),
                                  driver=self.config_dic.get('driver'),
                                  host=self.config_dic.get('host'),
                                  user=self.config_dic.get('user'),
                                  password=self.config_dic.get('password'))
            self.portlet_database.set_connected()
            
            # Save .ini-file automatically on connection
            if self.autosave == True:
                self.save_settings_to_ini()
        except Exception, inst:
            self.ErrorDialog.show(message='Datenbank konnte nicht verbunden werden.', instance=inst)
            self.portlet_database.set_disconnected()
        return self.database


    def disconnect(self):        
        if self.database.connection <> None:
            self.database.close()
        self.portlet_database.set_disconnected()
        
        