import wx
import res.Portlets

from res import IconSet16
from Buttons import BitmapToggleButton


class Database(res.Portlets.Database):
    def __init__(self, parent, autosave=False):
        """ If autosave = False, there is a save-button appearing! """
        
        # TODO: Save button for autosave has to be implemented! 
        res.Portlets.Database.__init__(self, parent)
        
        self.on_connect = None
        self.on_disconnect = None
        
        self.togglebutton_connect = BitmapToggleButton(self, \
            label_bitmap=IconSet16.getconnect_no_16Bitmap(), \
            selected_bitmap = IconSet16.getconnect_creating_16Bitmap()
        )
        
        self.togglebutton_connect.Bind(wx.EVT_BUTTON, self.on_togglebutton_connect_toggled) #, self.togglebutton_connect)
        self.sizer_button.Add( self.togglebutton_connect, 1, wx.ALIGN_RIGHT|wx.ALL, 5 )
        
        
    def on_togglebutton_connect_toggled(self, event):
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
    
    
    def populate(self, content_dict):
        """ content_dict = \
            {'engines_list':  ['SQLite'],
             'drivers_list':  ['list of drivers'],
             'engine':   'SQLite',
             'driver':   '',
             'database': 'customer.db',
             'host':     'hostname:port',
             'user':     'Mustermann',
             'password': '123456'}"""
        
        # Populate comboboxes -------------------------------------------------
        self.combobox_odbc.AppendItems(content_dict.get('drivers_list'))
        self.combobox_engine.AppendItems(content_dict.get('engines_list'))
        
        self.combobox_odbc.SetValue(content_dict.get('driver'))
        self.combobox_engine.SetValue(content_dict.get('engine'))
        self.entry_database.SetValue(content_dict.get('database'))
        self.entry_host.SetValue(content_dict.get('host'))
        self.entry_user.SetValue(content_dict.get('user'))
        self.entry_password.SetValue(content_dict.get('password'))
        
        
    def get_content(self):
        content_dict = {'engine': self.combobox_engine.GetValue(),
                        'driver': self.combobox_odbc.GetValue(),
                        'database': self.entry_database.GetValue(),
                        'host': self.entry_host.GetValue(),
                        'user': self.entry_user.GetValue(),
                        'password': self.entry_password.GetValue()}
        return content_dict
    
    
    def set_connected(self):
        print "now, i have to connect"
        
        
    def set_disconnected(self):
        print "yet, i have to disconnect"
        
        
        
        
        
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
            