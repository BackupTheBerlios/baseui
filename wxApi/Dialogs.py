# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wx.Dialogs module
# (c) by Mark Muzenhardt
#===============================================================================

import traceback
import wx
import res.Dialogs

from res import IconSet32
from pprint import pprint


class Error(res.Dialogs.Error):
    def __init__(self, parent):
        res.Dialogs.Error.__init__(self, parent)

        self.m_bitmap_icon.SetBitmap(IconSet32.geterror_32Bitmap())
        
        self.m_button_ok.Bind(wx.EVT_BUTTON, self.on_button_ok_clicked)
        self.m_toggleBtn_detail.Bind(wx.EVT_TOGGLEBUTTON, self.on_togglebutton_detail_toggled)


    def show(self, title='Fehler', instance=None, text='Error'):
        if instance <> None:
            detail = traceback.format_exc()
            self.m_textCtrl_traceback.SetValue(detail)
        
        self.m_staticText_text.SetLabel(text)
        self.SetTitle(title)
        
        self.ShowModal()


    def on_togglebutton_detail_toggled(self, event):
        is_down = event.IsChecked() 
        
        if is_down:
            self.m_textCtrl_traceback.Show()
        else:
            self.m_textCtrl_traceback.Hide()
        
        self.SetInitialSize()
        
            
    def on_button_ok_clicked(self, event):
        self.Hide()
        
        