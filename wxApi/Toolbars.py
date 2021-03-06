# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wx.Toolbars module
# by Mark Muzenhardt, published under LGPL license.
#===============================================================================

import wx

from res import IconSet16
from Buttons import BitmapTextToggleButton        


class FormToolbar(wx.ToolBar):
    def __init__(self, parent, preferences=True, help=True):
        wx.ToolBar.__init__(self, parent, id=-1, pos=wx.DefaultPosition, 
                            size=wx.DefaultSize, 
                            style=wx.TB_FLAT | wx.TB_NODIVIDER) 
        
        self.SetToolBitmapSize(wx.Size(22, 22))
               
        self.AddLabelTool(id=wx.ID_ANY, label="Speichern",  bitmap=IconSet16.getfilesave_16Bitmap())
        self.AddLabelTool(id=wx.ID_ANY, label="L�schen",    bitmap=IconSet16.getdelete_16Bitmap())
        
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
        
        self.sizer = wx.FlexGridSizer(len(self.content_lod), 1, 0, 0)
        self.sizer.AddGrowableCol(0)
        self.SetSizer(self.sizer)
        
        for content_dic in self.content_lod:
            bitmap = wx.Image(content_dic.get('picture'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            content_dic['button'] = BitmapTextToggleButton(self, label=content_dic.get('label'), bitmap=bitmap)
            content_dic['button'].Bind(wx.EVT_BUTTON, self.on_toggled)
            self.sizer.Add(content_dic['button'], 0, wx.ALL|wx.EXPAND)
        self.Show()
        
        # Initialize first button and fire an event which is none!
        self.content_lod[0]['button'].SetToggle(True)
        self.content_lod[0]['on_activate'](name=self.content_lod[0]['name'])

    
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
                    
                    
                
                
        