# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wx.Toolbars module
# (c) by Mark Muzenhardt
#===============================================================================

import wx

from res import IconSet16
from Buttons import BitmapTextToggleButton


class WebserverToolbar(wx.ToolBar):
    ID_START = 1
    ID_STOP = 2
    ID_PREFERENCES = 3
    ID_HELP = 4
    
    def __init__(self, parent, preferences=True, help=True):
        wx.ToolBar.__init__(self, parent, id=-1, pos=wx.DefaultPosition, 
                            size=wx.DefaultSize, 
                            style=wx.TB_FLAT | wx.TB_NODIVIDER)
        self.SetToolBitmapSize(wx.Size(22, 22))
        
        self.AddLabelTool(id=self.ID_START, label="Start", bitmap=IconSet16.getstart_16Bitmap())
        self.AddLabelTool(id=self.ID_STOP, label="Stop",  bitmap=IconSet16.getstop_16Bitmap())
        
        self.AddSeparator()
        if preferences == True:
            self.AddLabelTool(id=self.ID_PREFERENCES, label="Einstellungen", bitmap=IconSet16.getpreferences_16Bitmap())
        
        if help == True:
            self.AddLabelTool(id=self.ID_HELP, label="Hilfe", bitmap=IconSet16.gethelp_16Bitmap())

        self.Realize()
        
        
                            
class TableToolbar(wx.ToolBar):
    ID_NEW = 101
    ID_EDIT = 102
    ID_DELETE = 103
    
    ID_PRINT = 201
    
    ID_PREFERENCES = 401
    ID_HELP = 402
    
    
    def __init__(self, parent, filter=True, search=True, preferences=True, help=True):
        wx.ToolBar.__init__(self, parent, id=-1, pos=wx.DefaultPosition, 
                            size=wx.DefaultSize, 
                            style=wx.TB_FLAT | wx.TB_NODIVIDER)
        
        self.SetToolBitmapSize(wx.Size(22, 22))
        
        self.AddLabelTool(self.ID_NEW,    label="Neu",        bitmap=IconSet16.getfilenew_16Bitmap())
        self.AddLabelTool(self.ID_EDIT,   label="Bearbeiten", bitmap=IconSet16.getedit_16Bitmap())
        self.AddLabelTool(self.ID_DELETE, label=u"Löschen",   bitmap=IconSet16.getdelete_16Bitmap())
        
        self.AddSeparator()
        self.AddLabelTool(self.ID_PRINT, label="Drucken", bitmap=IconSet16.getprint_16Bitmap())
        
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
            self.AddLabelTool(self.ID_PREFERENCES, label="Einstellungen", bitmap=IconSet16.getpreferences_16Bitmap())
        
        if help == True:
            self.AddLabelTool(self.ID_HELP, label="Hilfe", bitmap=IconSet16.gethelp_16Bitmap())
        
        self.Realize()
        


class FormToolbar(wx.ToolBar):
    def __init__(self, parent, preferences=True, help=True):
        wx.ToolBar.__init__(self, parent, id=-1, pos=wx.DefaultPosition, 
                            size=wx.DefaultSize, 
                            style=wx.TB_FLAT | wx.TB_NODIVIDER) 
        
        self.SetToolBitmapSize(wx.Size(22, 22))
               
        self.AddLabelTool(id=wx.ID_ANY, label="Speichern",  bitmap=IconSet16.getfilesave_16Bitmap())
        self.AddLabelTool(id=wx.ID_ANY, label="Löschen",    bitmap=IconSet16.getdelete_16Bitmap())
        
        self.AddSeparator()
        self.AddLabelTool(id=wx.ID_ANY, label="Drucken", bitmap=IconSet16.getprint_16Bitmap())
            
        if preferences == True or help == True:
            self.AddSeparator()
        
        if preferences == True:
            self.AddLabelTool(id=-1, label="Einstellungen", bitmap=IconSet16.getpreferences_16Bitmap())
        
        if help == True:
            self.AddLabelTool(id=-1, label="Hilfe", bitmap=IconSet16.gethelp_16Bitmap())
        
        self.Realize()
        
        
        
class LookoutSidebar(wx.Panel):
    def __init__(self, parent, content_lod=None):
        """ content_lod = 
            [
                {'bitmap': wx.Bitmap, 'label': str, 'on_activate': func, 'id': 1},
            ]
        """
        
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.TAB_TRAVERSAL)
        self.content_lod = content_lod

        self.sizer = wx.FlexGridSizer(2, 1, 0, 0)
        self.sizer.AddGrowableCol(0)
        self.SetSizer(self.sizer)
        
        for content_dic in self.content_lod:
            bitmap = wx.Image(content_dic.get('picture'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            content_dic['button'] = BitmapTextToggleButton(self, label=content_dic.get('label'), bitmap=bitmap)
            content_dic['button'].Bind(wx.EVT_BUTTON, self.on_toggled)
            self.sizer.Add(content_dic['button'], 0, wx.ALL|wx.EXPAND)
        self.Show()
        
        self.content_lod[0]['button'].SetToggle(True)

    
    def on_toggled(self, event=None):
        button = event.GetButtonObj()
        for content_dic in self.content_lod:
            if content_dic['button'] <> button:
                content_dic['button'].SetToggle(False)
            else:
                function = content_dic.get('on_activate')
                if function <> None and button.GetToggle() == True:
                    name = content_dic.get('name')
                    function(event, name)
                if button.GetToggle() == False:
                    button.SetToggle(True)
                    
                    
                
                
        