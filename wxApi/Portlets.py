import wx
import resources.Portlets

from resources import Images
from Buttons import BitmapToggleButton


class Database(resources.Portlets.Database):
    def __init__(self, parent):
        resources.Portlets.Database.__init__(self, parent)

        self.connect_function = None
        self.disconnect_function = None
        
        self.togglebutton_connect = BitmapToggleButton(self, \
            label_bitmap=Images.getconnect_no_16Bitmap(), \
            selected_bitmap = Images.getconnect_creating_16Bitmap()
        )
        
        self.Bind(wx.EVT_BUTTON, self.on_togglebutton_connect_toggled, self.togglebutton_connect)
        self.sizer_button.Add( self.togglebutton_connect, 1, wx.ALIGN_RIGHT, 5 )
        
        
    def on_togglebutton_connect_toggled(self, event):
        print event
        
        
        
class Login(resources.Portlets.Login):
    def __init__(self, parent):
        resources.Portlets.Login.__init__(self, parent)
        