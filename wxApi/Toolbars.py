# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wx.Toolbars module
# (c) by Mark Muzenhardt
#===============================================================================

import wx

from res import IconSet16
from Buttons import BitmapTextToggleButton


class DatasetToolbar(wx.ToolBar):
    def __init__(self, parent, filter=False, search=False, preferences=False, help=True):
        wx.ToolBar.__init__(self, parent, id=-1, pos=wx.DefaultPosition, 
                            size=wx.DefaultSize, 
                            style=wx.TB_FLAT | wx.TB_NODIVIDER)
        
        self.SetToolBitmapSize(wx.Size(22, 22))
        
        self.AddLabelTool(id=-1, label="Neu",        bitmap=IconSet16.getfilenew_16Bitmap())
        self.AddLabelTool(id=-1, label="Bearbeiten", bitmap=IconSet16.getedit_16Bitmap())
        self.AddLabelTool(id=-1, label=u"Löschen",   bitmap=IconSet16.getdelete_16Bitmap())
        
        self.AddSeparator()
        self.AddLabelTool(id=-1, label="Drucken",       bitmap=IconSet16.getprint_16Bitmap())
        
        if filter == True:
            self.AddSeparator()
            self.combobox_filter = wx.ComboBox(
                parent=self, id=-1, choices=["", "This", "is a", "wx.ComboBox"],
                size=(150,-1), style=wx.CB_DROPDOWN)
            self.AddControl(self.combobox_filter)
        
        if search == True:   
            self.AddSeparator() 
            self.entry_search = wx.SearchCtrl(parent=self, id=-1)
            self.AddControl(self.entry_search) 
            
        if preferences == True or help == True:
            self.AddSeparator()
        
        if preferences == True:
            self.AddLabelTool(id=-1, label="Einstellungen", bitmap=IconSet16.getpreferences_16Bitmap())
        
        if help == True:
            self.AddLabelTool(id=-1, label="Hilfe",         bitmap=IconSet16.gethelp_16Bitmap())
        
        self.Realize()
        


class LookoutSidebar(wx.Panel):
    def __init__(self, parent, content_lod=None):
        """ content_lod = 
            [
                {'bitmap': wx.Bitmap, 'label': str, 'on_activate': func},
            ]
        """
        
        wx.Panel.__init__(self, parent, id=-1)
        
        BitmapTextToggleButton(parent, label)