# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wxConfigWidgets module.
# by Mark Muzenhardt, published under LGPL license.
#===============================================================================

import wx, wx.xrc
import json

from wxApi import DataViews
from misc.FileSystem import iniFile
from wxApi.Widgets import widget_populator, widget_getter
from pprint import pprint


class JsonTable(wx.Panel):
    ''' used for PythonServer '''
    
    def __init__(self, json_filepath, form=None, portlet_parent=None, editable=True, permissions={}):
        self.json_filepath = json_filepath
        self.form = form
        self.portlet_parent = portlet_parent
        self.parent_form = None
        self.content_lod = []
        
    
    def on_add_clicked(self, event):
        print 'add'
        
        
    def on_edit_clicked(self, event):
        print 'edit'
        
        
    def on_delete_clicked(self, event):
        print 'delete'
        
        
    def initialize(self, definition_lod=None):
        self.definition_lod = definition_lod
    
    
    def populate(self, content_lod=None):
        try:
            file = open(self.json_filepath, 'rb')
            self.content_lod = json.load(file)
        except:
            file = open(self.json_filepath, 'wb')
            json.dump([], file)
            file.close()
            
            file = open(self.json_filepath, 'rb')
            self.content_lod = json.load(file)
        
        self.Table.populate(self.content_lod)
                
    
    def create(self):
        # Just creates a panel to draw the Table on, that buttons or else can be 
        # attached near the Table!
        
        self.panel_main = wx.Panel(self.portlet_parent)
        sizer = self.portlet_parent.GetSizer()
        sizer.Add(self.panel_main, 0, wx.ALL|wx.EXPAND)
        
        self.sizer_main = wx.FlexGridSizer(1, 2, 0, 0)
        self.sizer_main.AddGrowableCol(0)
        self.sizer_main.AddGrowableRow(0)
        self.sizer_main.SetFlexibleDirection( wx.BOTH )
        self.sizer_main.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        self.panel_main.SetSizer(self.sizer_main)
        
        self.Table = DataViews.Tree(self.panel_main)
        self.sizer_buttons = wx.BoxSizer(wx.VERTICAL)
        
        self.button_add = wx.Button(self.panel_main, wx.ID_ANY, u'Hinzufügen')
        self.sizer_buttons.Add(self.button_add, 0, wx.ALL, 5)
        self.button_add.Bind(wx.EVT_BUTTON, self.on_add_clicked)
        
        self.button_edit = wx.Button(self.panel_main, wx.ID_ANY, u'Bearbeiten')
        self.sizer_buttons.Add(self.button_edit, 0, wx.ALL, 5)
        self.button_edit.Bind(wx.EVT_BUTTON, self.on_edit_clicked)
        
        self.button_delete = wx.Button(self.panel_main, wx.ID_ANY, u'Entfernen')
        self.sizer_buttons.Add(self.button_delete, 0, wx.ALL, 5)
        self.button_delete.Bind(wx.EVT_BUTTON, self.on_delete_clicked)
        
        self.sizer_main.Add(self.Table, 0, wx.ALL|wx.EXPAND)        
        self.sizer_main.Add(self.sizer_buttons)
        self.Table.initialize(definition_lod=self.definition_lod) #, attributes_lod=self.attributes_lod)
        
        # Just populate immideately if this is not a child-table of a form!
        if self.parent_form == None:
            self.populate()
        
        self.Table.Show()       
        return self.panel_main
        
        
        
class JsonForm(DataViews.Form):
    def __init__(self, parent, xrc_path, panel_name):
        DataViews.Form.__init__(self, parent, xrc_path, panel_name)
        
        
        
class IniDialog(wx.Dialog):
    ''' used for PythonServer '''
    
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
            widget_populator(widget_object, value, None)
        
                
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
        
        
        
class ConfigDialog(wx.Dialog):
    def __init__(self, parent, db_object):
        self.db_object = db_object
        
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = 'Einstellungen', pos = wx.DefaultPosition, size = wx.Size(600, 400), style = wx.DEFAULT_DIALOG_STYLE )
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        sizer_main = wx.FlexGridSizer( 2, 1, 0, 0 )
        sizer_main.AddGrowableCol( 0 )
        sizer_main.AddGrowableRow( 0 )
        sizer_main.SetFlexibleDirection( wx.BOTH )
        sizer_main.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NB_MULTILINE )
        
        
        #self.panel_globals = form_globals(parent=self.notebook, xrc_path=RESOURCE_DIR + 'forms.xrc', panel_name='panel_globals')
        #self.notebook.AddPage(self.panel_globals, 'Allgemein', False)
        
        # Do the buttons and the rest
        sizer_main.Add( self.notebook, 1, wx.EXPAND |wx.ALL, 5 )
        
        sizer_buttons = wx.FlexGridSizer( 2, 2, 0, 0 )
        sizer_buttons.SetFlexibleDirection( wx.BOTH )
        sizer_buttons.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.button_ok = wx.Button( self, wx.ID_ANY, u"Ok", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.button_ok.Bind(wx.EVT_BUTTON, self.on_button_ok_clicked, id=wx.ID_ANY)
        sizer_buttons.Add( self.button_ok, 0, wx.ALL, 5 )
        
        sizer_main.Add( sizer_buttons, 0, wx.ALIGN_RIGHT, 5 )
        
        self.SetSizer(sizer_main)
        self.Layout()
        
        self.Centre(wx.BOTH)
        
        
    def __del__( self ):
        pass
        
        
    def on_button_ok_clicked(self, event=None):
        self.Close()
        
        
    def add_panel(self, title, db_table, table, form):
        db_table_object = db_table(self.db_object)
        panel = wx.Panel( self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        table_object = table(db_table=db_table_object, form_object=form, portlet_parent=panel)
        
        table_object.create()
        panel.Layout()
        self.notebook.AddPage(panel, title, False)
        
        
        
