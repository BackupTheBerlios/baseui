# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wxPanels module.
# published under LGPL license by Mark Muzenhardt.
#===============================================================================

import wx

from wxApi import Panels, Dialogs
from misc.FileSystem import iniFile
from dbApi import SQLdb, Tools as dbTools


class Database(Panels.Database):
    def __init__(self, parent, ini_path, ini_section, autosave=False, 
                 db_table_users_class=None):
        Panels.Database.__init__(self, parent)
        self.ErrorDialog = Dialogs.Error(self)
        
        self.ini_file = iniFile(ini_path)
        self.ini_section = ini_section
        self.autosave = autosave
        self.db_table_users_class = db_table_users_class
        
        # Get the database settings -------------------------------------------
        self.connect_functions_list = []
        self.disconnect_functions_list = []
        
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
        
    
    def add_connect_function(self, function):
        self.connect_functions_list.append(function)
        
        
    def add_disconnect_function(self, function):
        self.disconnect_functions_list.append(function)
        
        
    def get_database(self):
        return self.database
        
    
    def get_connection(self):
        return self.database.__dict__.get('connection')
        
    
    def set_connected(self):
        ''' This sets buttons and every other thing connected. '''
        
        super(Database, self).set_connected()
        for function in self.connect_functions_list:    
            function()
                
                
    def set_disconnected(self):
        ''' Sets all buttons and other things to disconnected. '''
        
        super(Database, self).set_disconnected()
        for function in self.disconnect_functions_list:
            function()
            
            
    def connect(self):
        ''' Trys to connect the database with given parameters. '''
        
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
        ''' Disconnects the database and closes the connection. '''
        
        if self.database.connection <> None:
            self.database.close()
        self.set_disconnected()
        return self.database
        
        
    def save_settings(self):
        self.ini_file.save_section(self.ini_section, self.section_dict)

        
       
class DatabaseLogin(wx.Panel):
    def __init__(self, parent, image_path, ini_path, ini_section, autosave=True, db_table_users_class=None, db_table_system_class=None):
        wx.Panel.__init__(self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, style = wx.TAB_TRAVERSAL)
        self.ErrorDialog = Dialogs.Error(parent=self)
        
        self.image_path = image_path
        self.ini_path = ini_path
        self.ini_section = ini_section
        self.autosave = autosave
        self.db_table_users_class = db_table_users_class
        self.db_table_system_class = db_table_system_class
        
        self.on_connect = None
        self.on_disconnect = None
        
        self.sizer = wx.FlexGridSizer( 3, 1, 0, 0 )
        self.sizer.AddGrowableCol( 0 )
        self.sizer.AddGrowableRow( 0, 1 )
        
        self.sizer.SetFlexibleDirection( wx.BOTH )
        self.sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.portlet_database = Database(parent=self, 
                                         ini_path=self.ini_path, 
                                         ini_section=self.ini_section,
                                         autosave=self.autosave,
                                         db_table_users_class=self.db_table_users_class)
        self.portlet_database.Hide()
        self.portlet_login = Panels.Login(parent=self)
        
        png = wx.Image(self.image_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.logo = wx.StaticBitmap(self, -1, png, (10, 5), (png.GetWidth(), png.GetHeight()))
        
        self.sizer.Add(self.logo, 0, wx.ALL|wx.EXPAND)
        self.sizer.Add(self.portlet_login, 0, wx.ALL|wx.EXPAND)
        
        self.SetSizer(self.sizer)
        self.Layout()
        self.SetInitialSize()
        
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
        
        self.portlet_database.add_connect_function(self.set_connected)
        self.portlet_database.add_disconnect_function(self.set_disconnected)
        
        self.portlet_login.combobox_user.Bind(wx.EVT_TEXT, self.on_login_changed)
        self.portlet_login.entry_password.Bind(wx.EVT_TEXT, self.on_login_changed)
        
        
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
        
        
    def on_login_changed(self, event=None):
        userdata = self.get_userdata()
        password = self.portlet_login.entry_password.GetValue()
        choises = self.portlet_login.combobox_user.GetStrings()
        
        if userdata == None:
            if choises == []:
                self.button_ok.Enable(True)
            else:
                self.button_ok.Enable(False)
            return
        
        if password == userdata.get('password') or \
           userdata.get('password') == None:
            self.button_ok.Enable(True)
        else:
            self.button_ok.Enable(False)
        
        
    # Actions -----------------------------------------------------------------
    def get_database(self):
        self.database = self.portlet_database.get_database()
        return self.database
        
    
    def get_userdata(self):
        text = self.portlet_login.combobox_user.GetValue()
        selection = self.portlet_login.combobox_user.FindString(text)
        if selection == -1:
            return
        return self.portlet_login.combobox_user.GetClientData(selection)
        
        
    def get_settings(self):
        return self.db_table_system.get_content()
    
    
    def get_connection(self):
        return self.portlet_database.get_connection()
        
    
    def set_connected(self):
        if self.db_table_system_class <> None:
            self.db_table_system = self.db_table_system_class(self.get_database())
            
        self.db_table_users = self.db_table_users_class(self.get_database())
        result = self.db_table_users.select()
        self.portlet_login.combobox_user.Clear()
        for dict in result:
            choise = dict.get('username')
            if choise == None:
                choise = ''
            self.portlet_login.combobox_user.Append(choise, dict)
            
        self.portlet_login.combobox_user.Enable(True)
        self.portlet_login.entry_password.Enable(True)
        self.on_login_changed()
        
    
    def set_disconnected(self):
        self.portlet_login.combobox_user.Enable(False)
        self.portlet_login.entry_password.Enable(False)
        self.button_ok.Enable(False)
        
        
    def connect(self):
        self.database = self.portlet_database.connect()

    
    def disconnect(self):        
        self.database = self.portlet_database.disconnect()
        
        
        

        
    