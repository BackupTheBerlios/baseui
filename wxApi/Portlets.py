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
        self.sizer_button.Add( self.togglebutton_connect, 1, wx.ALIGN_RIGHT, 5 )
        
        
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
            
        
        
class Login(res.Portlets.Login):
    def __init__(self, parent):
        res.Portlets.Login.__init__(self, parent)
        
        
        