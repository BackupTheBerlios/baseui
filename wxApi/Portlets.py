import wx
import res.Portlets

from res import IconSet16
from Buttons import BitmapToggleButton


class Database(res.Portlets.Database):
    def __init__(self, parent):
        res.Portlets.Database.__init__(self, parent)

        self.connect_function = None
        self.disconnect_function = None
        
        self.togglebutton_connect = BitmapToggleButton(self, \
            label_bitmap=IconSet16.getconnect_no_16Bitmap(), \
            selected_bitmap = IconSet16.getconnect_creating_16Bitmap()
        )
        
        self.togglebutton_connect.Bind(wx.EVT_BUTTON, self.on_togglebutton_connect_toggled) #, self.togglebutton_connect)
        self.sizer_button.Add( self.togglebutton_connect, 1, wx.ALIGN_RIGHT, 5 )
        
        
    def on_togglebutton_connect_toggled(self, event):
        print event
        
        
        
class Login(res.Portlets.Login):
    def __init__(self, parent):
        res.Portlets.Login.__init__(self, parent)
        
        
        