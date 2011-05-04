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
    def __init__(self, json_filepath, form=None, portlet_parent=None, editable=True, permissions={}):
        self.json_filepath = json_filepath
        self.form = form
        self.portlet_parent = portlet_parent
        self.parent_form = None
        self.content_lod = []
        
        
    def initialize(self, definition_lod=None):
        self.definition_lod = definition_lod
    
    
    def populate(self, content_lod=None):
        self.Table.populate(self.content_lod)
    
    
    def populate_portlet(self):
        # Just creates a panel to draw the Table on, that buttons or else can be 
        # attached near the Table!
        
        self.main_panel = wx.Panel(self.portlet_parent)
        sizer = self.portlet_parent.GetSizer()
        sizer.Add(self.main_panel, 0, wx.ALL|wx.EXPAND)
        
        self.main_sizer = wx.FlexGridSizer(1, 2, 0, 0)
        self.main_sizer.AddGrowableCol(0)
        self.main_sizer.AddGrowableRow(0)
        self.main_sizer.SetFlexibleDirection( wx.BOTH )
        self.main_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        self.main_panel.SetSizer(self.main_sizer)
        
        self.Table = DataViews.Tree(self.main_panel)
        self.button_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.button_new = wx.Button(self.main_panel, wx.ID_ANY, u'Neu')
        self.button_sizer.Add(self.button_new, 0, wx.ALL, 5)
        
        self.button_delete = wx.Button(self.main_panel, wx.ID_ANY, u'L�schen')
        self.button_sizer.Add(self.button_delete, 0, wx.ALL, 5)
        
        
        #self.button_import = wx.Button(self.main_panel, wx.ID_ANY, u'Import')
        #self.button_import
        #self.Table.row_right_click_function = self.row_right_click_function
        
        self.main_sizer.Add(self.Table, 0, wx.ALL|wx.EXPAND)        
        self.main_sizer.Add(self.button_sizer)
        self.Table.initialize(definition_lod=self.definition_lod) #, attributes_lod=self.attributes_lod)
        #self.Table.set_row_activate_function(self.on_row_activate)
        #self.Table.set_cursor_change_function(self.on_cursor_changed)
        
        # Just populate immideately if this is not a child-table of a form!
        if self.parent_form == None:
            self.populate()

        self.Table.Show()       
        return self.main_panel
        
        
    
    
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
        
        self.button_apply = wx.Button(bottom_panel, label=u'�bernehmen')
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



