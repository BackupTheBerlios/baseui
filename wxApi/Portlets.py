import wx
import res.Portlets

from res import IconSet16
from Buttons import BitmapToggleButton


class Database(res.Portlets.Database):
    def __init__(self, parent):
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
            {'engines':      ['SQLite'],
             'database':     'customer.db',
             'odbc_drivers': ['list of drivers'],
             'host':         'hostname:port',
             'user':         'Mustermann',
             'password':     '123456'}"""
        
        # Populate comboboxes -------------------------------------------------
        self.combobox_odbc.AppendItems(content_dict.get('odbc_drivers'))
        self.combobox_engine.AppendItems(content_dict.get('engines'))
        
        
    def get_content(self):
        content_dict = {'engine': self.combobox_engine.GetStringSelection(),
                        'odbc_driver': self.combobox_odbc.GetStringSelection(),
                        'database': self.entry_database.GetValue(),
                        'host': self.entry_host.GetValue(),
                        'user': self.entry_user.GetValue(),
                        'password': self.entry_password.GetValue()}
        return content_dict
        
        
        
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
            