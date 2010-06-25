import wx

from wx.lib.buttons import GenBitmapToggleButton


class BitmapToggleButton(GenBitmapToggleButton):
    def __init__(self, parent, label_bitmap=None, selected_bitmap=None, toggled=False):
        # An image toggle button
        GenBitmapToggleButton.__init__(self, parent, id=-1, bitmap=None)
        
        if label_bitmap <> None:
            mask = wx.Mask(label_bitmap, wx.BLUE)
            label_bitmap.SetMask(mask)
            self.SetBitmapLabel(label_bitmap)
        
        if selected_bitmap <> None:
            mask = wx.Mask(selected_bitmap, wx.BLUE)
            selected_bitmap.SetMask(mask)
            self.SetBitmapSelected(selected_bitmap)
        
        self.SetToggle(toggled)
        self.SetInitialSize()
