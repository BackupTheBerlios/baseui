# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wxPortlets module.
# by Mark Muzenhardt, published under LGPL license.
#===============================================================================

import wx, wx.xrc

from wxApi import DataViews
from misc.FileSystem import iniFile
from wxApi.Widgets import widget_populator, widget_getter
from pprint import pprint


class JsonTable(wx.Panel):
    def __init__(self, parent):
        
        DataViews.Tree.__init__(self, parent)
        
        
        
    
    
class IniDialog(wx.Dialog):
    ID_CANCEL = 101
    ID_OK = 102
    
    def __init__(self, parent, ini_path='', xrc_path='', xrc_panel=''):
        wx.Dialog.__init__ (self, parent, wx.ID_ANY, 'Einstellungen', size=(600,400))
        
        self.iniFile = iniFile(ini_path)
        
        self.sizer = wx.FlexGridSizer( 2, 1, 0, 0 )
        self.sizer.AddGrowableCol( 0 )
        self.sizer.AddGrowableRow( 0, 1 )
        self.sizer.SetFlexibleDirection( wx.BOTH )
        self.sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.xrc_resource = wx.xrc.XmlResource(xrc_path)
        panel = self.xrc_resource.LoadPanel(self, xrc_panel)
        self.sizer.Add(panel, 0, wx.ALL|wx.EXPAND)
        
        # Bottom panel --------------------------------------------------------
        bottom_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.sizer.Add(bottom_panel, 1, wx.ALL|wx.EXPAND)
        
        bottom_sizer = wx.FlexGridSizer( 0, 3, 0, 0 )
        bottom_sizer.AddGrowableCol( 0 )
        bottom_sizer.AddGrowableRow( 0 )
        
        self.button_ok = wx.Button(bottom_panel, label='Ok')
        bottom_sizer.Add(self.button_ok, 1, wx.ALL|wx.ALIGN_RIGHT, 5)
        self.button_ok.Bind(wx.EVT_BUTTON, self.on_ok)
        
        self.button_cancel = wx.Button(bottom_panel, label='Abbrechen')
        bottom_sizer.Add(self.button_cancel, 1, wx.ALL|wx.ALIGN_RIGHT, 5)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
        
        self.button_apply = wx.Button(bottom_panel, label=u'Übernehmen')
        bottom_sizer.Add(self.button_apply, 1, wx.ALL|wx.ALIGN_RIGHT, 5)
        self.button_apply.Bind(wx.EVT_BUTTON, self.on_apply)

        bottom_panel.SetSizer(bottom_sizer)
        
        # Add that stuff to the Dialog ----------------------------------------
        self.SetSizer(self.sizer)
        self.Layout()
    

    def on_ok(self, event=None):
        self.save()
        self.Close()
        
    
    def on_apply(self, event=None):
        self.button_apply.Disable()
        self.save()
        
        
    def on_cancel(self, event=None):
        self.save()
        self.Close()
        
    
    def initialize(self, definition_lod):
        self.definition_lod = definition_lod
        
        for definition_dict in self.definition_lod:
            widget_name = definition_dict['widget_name']
            
            if widget_name <> None:
                widget_object = wx.xrc.XRCCTRL(self, widget_name)
                definition_dict['widget_object'] = widget_object
        self.populate()
        

    def populate(self):
        for definition_dict in self.definition_lod:
            widget_object = definition_dict.get('widget_object')
            
            section = definition_dict.get('section')
            option = definition_dict.get('option')
            default = definition_dict.get('default')
            
            value = self.iniFile.get_option(section, option, default)
            widget_object = definition_dict.get('widget_object')
            widget_populator(widget_object, value)
        
                
    def save(self):
        for definition_dict in self.definition_lod:
            value = widget_getter(definition_dict.get('widget_object'))
            if value == None:
                value = ''
            if value == False:
                value = 0
            if value == True:
                value = 1
            definition_dict['value'] = value
            
        self.iniFile.save_lod(self.definition_lod)



