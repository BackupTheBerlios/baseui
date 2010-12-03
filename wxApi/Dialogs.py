# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wx.Dialogs module
# (c) by Mark Muzenhardt
#===============================================================================

import traceback
import wx
import res.Dialogs
from res import IconSet32


class Help(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)



class Error(res.Dialogs.Error):
    def __init__(self, parent):
        res.Dialogs.Error.__init__(self, parent)
        
        self.m_bitmap_icon.SetBitmap(IconSet32.geterror_32Bitmap())
        
        self.button_ok.Bind(wx.EVT_BUTTON, self.on_button_ok_clicked)
        self.togglebutton_detail.Bind(wx.EVT_TOGGLEBUTTON, self.on_togglebutton_detail_toggled)
        
        
    def show(self, title='Fehler', instance=None, message='Error'):
        self.togglebutton_detail.SetValue(False)
        if instance <> None:
            detail = traceback.format_exc()
            self.entry_traceback.SetValue(detail)
        
        self.m_staticText_text.SetLabel(message)
        self.SetTitle(title)
        
        self.SetInitialSize()
        self.Centre()
        self.ShowModal()
        
        
    def on_togglebutton_detail_toggled(self, event):
        is_down = event.IsChecked() 
        
        if is_down:
            self.entry_traceback.Show()
            self.staticline_bottom.Show()
        else:
            self.entry_traceback.Hide()
            self.staticline_bottom.Hide()
            
        self.SetInitialSize()
        
        
    def on_button_ok_clicked(self, event):
        self.entry_traceback.Hide()
        self.Hide()
        
        
        
class FormTablePreferences(wx.Dialog):
    ID_IMPORT = 201
    ID_EXPORT = 202
    
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title)
        