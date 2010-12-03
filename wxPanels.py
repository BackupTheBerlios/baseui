# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wxPortlets module.
# published under BSD license by Mark Muzenhardt.
#===============================================================================

import wx

from wxApi import Panels, Dialogs
from misc.FileSystem import iniFile
from dbApi import SQLdb, Tools as dbTools


class Database(Panels.Database):
    def __init__(self, parent, ini_path, ini_section, autosave=False):
        Panels.Database.__init__(self, parent)
        self.ErrorDialog = Dialogs.Error(self)
        
        self.ini_file = iniFile(ini_path)
        self.ini_section = ini_section
        self.autosave = autosave
        
        # Get the database settings -------------------------------------------
        self.database = None
        self.initialize()
        
        
    def initialize(self, event=None):
        # Populate comboboxes -------------------------------------------------
        odbc_drivers_list = dbTools.get_odbc_drivers()
        self.combobox_odbc.AppendItems(odbc_drivers_list)
        
        db_engines_list = SQLdb.get_engines()
        self.combobox_engine.AppendItems(db_engines_list)
        
        # Populate the rest ---------------------------------------------------
        options ={'engine': '', 
                  'driver': '', 
                  'database': '', 
                  'host': '', 
                  'user': '', 
                  'password': '', 
                  'filepath': ''}
        
        self.section_dict = self.ini_file.get_section(section=self.ini_section, option_dict=options)
        
        self.form_dict = {'engines_list': db_engines_list,
                          'drivers_list': odbc_drivers_list}
        self.form_dict.update(self.section_dict)
        self.populate(self.form_dict)
        
        self.on_connect = self.connect
        self.on_disconnect = self.disconnect
        
    
    def get_database(self):
        return self.database
        
        
    def connect(self):
        try:
            self.section_dict = self.get_content()
            self.database = SQLdb.database(self.section_dict.get('engine'))
            self.database.connect(database=self.section_dict.get('database'),
                                  driver=self.section_dict.get('driver'),
                                  host=self.section_dict.get('host'),
                                  user=self.section_dict.get('user'),
                                  password=self.section_dict.get('password'),
                                  filepath=self.section_dict.get('filepath'))
            self.set_connected()
            
            # Save .ini-file automatically on connection
            if self.autosave == True:
                self.save_settings()
        except Exception, inst:
            self.set_disconnected()
            self.ErrorDialog.show(message='Datenbank konnte nicht verbunden werden.', instance=inst)
        return self.database
        
        
    def disconnect(self):        
        if self.database.connection <> None:
            self.database.close()
        self.set_disconnected()
        return self.database
        
        
    def save_settings(self):
        self.ini_file.save_section(self.ini_section, self.section_dict)

        
       
class DatabaseLogin(wx.Panel):
    def __init__(self, parent, image_path, ini_path, ini_section, autosave=True):
        wx.Panel.__init__(self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 200,460 ), style = wx.TAB_TRAVERSAL)
        self.ErrorDialog = Dialogs.Error(parent=self)
        
        self.image_path = image_path
        self.ini_path = ini_path
        self.ini_section = ini_section
        self.autosave = autosave
        
        self.on_connect = None
        self.on_disconnect = None
        
        self.sizer = wx.FlexGridSizer( 2, 1, 0, 0 )
        self.sizer.AddGrowableCol( 0 )
        self.sizer.AddGrowableRow( 0, 1 )
        
        self.sizer.SetFlexibleDirection( wx.BOTH )
        self.sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.portlet_database = Database(parent=self, 
                                         ini_path=self.ini_path, 
                                         ini_section=self.ini_section,
                                         autosave=self.autosave)
        self.portlet_database.Hide()
        self.portlet_login = Panels.Login(parent=self)
        
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
    def get_database(self):
        self.database = self.portlet_database.get_database()
        return self.database
        
        
    def connect(self):
        self.database = self.portlet_database.connect()


    def disconnect(self):        
        self.database = self.portlet_database.disconnect()
        
        
        
class PreferencesDialog(wx.Frame):
    ''' Gesucht wird ein Dialog, der über ein einfaches LOD weitgehend definierbar
        ist. Optionen sind immer über ein TabNotebook erreichbar, jedes davon ist 
        eine section in der .ini-Datei. Jedes Notebook-Tab enthält ein Formular, 
        welches alle Optionen der jeweiligen section enthält. '''
        
    def __init__(self, ini_filepath):
        ''' definition_lod = [{'section_name': 'printer',  'label': 'Drucker', 'portlet_object': form(), 'icon_path': '/res/icon.ico'},
                              {'section_name': 'template', 'label': 'Vorlage', 'portlet_object': form(), 'icon_path': '/usr/chil.ico'}] '''
                              
        pass
    