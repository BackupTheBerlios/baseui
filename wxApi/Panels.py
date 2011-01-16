#===============================================================================
# BaseUI.wxApi.Panels
# by Mark Muzenhardt, published under LGPL license.
#===============================================================================

import wx
import res.Portlets

from res import IconSet16
from Buttons import BitmapToggleButton


class Database(res.Portlets.Database):
    def __init__(self, parent):
        """ If autosave = False, there is a save-button appearing! """
        
        # TODO: Save button for autosave has to be implemented! 
        res.Portlets.Database.__init__(self, parent)
        
        self.engines_list = []
        self.drivers_list = [] 
        
        self.on_connect = None
        self.on_disconnect = None
        
        self.combobox_engine.Bind(wx.EVT_TEXT, self.on_combobox_engine_changed)
        self.combobox_odbc.Bind(wx.EVT_TEXT, self.on_combobox_odbc_changed)
        
        self.togglebutton_connect = BitmapToggleButton(self, \
            label_bitmap=IconSet16.getconnect_no_16Bitmap(), \
            selected_bitmap = IconSet16.getconnect_creating_16Bitmap()
        )

        self.togglebutton_connect.Bind(wx.EVT_BUTTON, self.on_togglebutton_connect_toggled)
        self.sizer_button.Add(self.togglebutton_connect, 1, wx.ALIGN_RIGHT|wx.ALL, 5)

    
    def on_combobox_engine_changed(self, event=None):
        self.set_visibility()
         
    
    def on_combobox_odbc_changed(self, event=None):
        self.set_visibility()
        
        
    def on_togglebutton_connect_toggled(self, event=None):
        is_down = event.GetIsDown() 
        
        if is_down:
            if self.on_connect <> None:
                try:
                    self.on_connect()
                except:
                    raise
        else:
            if self.on_disconnect <> None:
                try:
                    self.on_disconnect()
                except:
                    raise
    
    
    def set_enabled(self, enabled=False):
        self.combobox_odbc.Enable(enabled)
        self.label_odbc.Enable(enabled)
        
        self.combobox_engine.Enable(enabled)
        self.label_engine.Enable(enabled)
        
        self.entry_database.Enable(enabled)
        self.label_database.Enable(enabled)
        
        self.entry_host.Enable(enabled)
        self.label_host.Enable(enabled)
        
        self.entry_user.Enable(enabled)
        self.label_user.Enable(enabled)
        
        self.entry_password.Enable(enabled)
        self.label_password.Enable(enabled)
        
        self.label_path.Enable(enabled)
        self.filepicker_path.Enable(enabled)
        
        
    def set_visibility(self):
        driver = self.combobox_odbc.GetValue()
        engine = self.combobox_engine.GetValue()
        
        odbc=False
        database=False
        host=False
        user=False
        password=False
        filepath=False
        
        if engine.lower() == 'odbc':
            odbc=True
            if '*.' in driver.lower():
                filepath=True
            elif driver in self.drivers_list:
                database=True
                host=True
                user=True
                password=True
        elif engine.lower() == 'sqlite':
            filepath=True
        elif engine in self.engines_list:
            database=True
            host=True
            user=True
            password=True

        self.combobox_odbc.Show(odbc)
        self.label_odbc.Show(odbc)
        
        self.entry_database.Show(database)
        self.label_database.Show(database)
        
        self.entry_host.Show(host)
        self.label_host.Show(host)
        
        self.entry_user.Show(user)
        self.label_user.Show(user)
        
        self.entry_password.Show(password)
        self.label_password.Show(password)
        
        self.label_path.Show(filepath)
        self.filepicker_path.Show(filepath)
        
        self.Layout()
        
        
    def populate(self, content_dict):
        """ content_dict = \
            {'engines_list':  ['SQLite'],
             'drivers_list':  ['list of drivers'],
             'engine':   'SQLite',
             'driver':   '',
             'database': 'customer.db',
             'host':     'hostname:port',
             'user':     'Mustermann',
             'password': '123456',
             'filepath': 'c:\access\test.mdb'}"""
        
        # Populate comboboxes -------------------------------------------------
        self.combobox_odbc.Clear()
        self.drivers_list = content_dict.get('drivers_list')
        self.combobox_odbc.AppendItems(self.drivers_list)
        
        self.combobox_engine.Clear()
        self.engines_list = content_dict.get('engines_list')
        self.combobox_engine.AppendItems(self.engines_list)
        
        # Populate the rest ---------------------------------------------------
        self.combobox_engine.SetValue(content_dict.get('engine'))
        self.on_combobox_engine_changed()
        
        self.combobox_odbc.SetValue(content_dict.get('driver'))
        self.on_combobox_odbc_changed()
        
        self.entry_database.SetValue(content_dict.get('database'))
        self.entry_host.SetValue(content_dict.get('host'))
        self.entry_user.SetValue(content_dict.get('user'))
        self.entry_password.SetValue(content_dict.get('password'))
        
        filepath = content_dict.get('filepath')
        if filepath == None: filepath = ''
        self.filepicker_path.SetPath(filepath)
        
        
    def get_content(self):
        content_dict = {'engine': self.combobox_engine.GetValue(),
                        'driver': self.combobox_odbc.GetValue(),
                        'database': self.entry_database.GetValue(),
                        'host': self.entry_host.GetValue(),
                        'user': self.entry_user.GetValue(),
                        'password': self.entry_password.GetValue(),
                        'filepath': self.filepicker_path.GetTextCtrlValue()}
        return content_dict
    
    
    def set_connected(self):
        bitmap = IconSet16.getconnect_established_16Bitmap()
        self.togglebutton_connect.SetBitmapSelected(bitmap)
        
        self.togglebutton_connect.SetToggle(True)
        self.set_enabled(False)
        
        
    def set_disconnected(self):
        bitmap = IconSet16.getconnect_no_16Bitmap()
        self.togglebutton_connect.SetBitmapLabel(bitmap)
        
        bitmap = IconSet16.getconnect_creating_16Bitmap()
        self.togglebutton_connect.SetBitmapSelected(bitmap)
        
        self.togglebutton_connect.SetToggle(False)
        self.set_enabled(True)
        
        
        
class Login(res.Portlets.Login):
    def __init__(self, parent):
        res.Portlets.Login.__init__(self, parent)
        
        
    def populate(self, content_lod):
        """ content_lod = \
            [
                {'user': 'Mustermann, Max', 'password': '123456'}
            ] """
        
        for content in content_lod:
            user_list.append(content.get('user'))
            
            

class TableImport(res.Portlets.TableImport):
    def __init__(self, parent):
        res.Portlets.TableImport.__init__(self, parent)
        
        
        
class TableExport(res.Portlets.TableExport):
    def __init__(self, parent):
        res.Portlets.TableExport.__init__(self, parent)
        
        
        
class TableConfig(res.Portlets.TableConfig):
    def __init__(self, parent):
        res.Portlets.TableConfig.__init__(self, parent)
        
        
        
class Webserver(res.Portlets.Webserver):
    def __init__(self, parent):
        res.Portlets.Webserver.__init__(self, parent)
        
        
    def populate(self, content_lod):
        pass
        
        
    