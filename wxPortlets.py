# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wxPortlets module.
# by Mark Muzenhardt, published under GPL license.
#===============================================================================

import wx, wx.aui

from misc import FileSystem, HelpFile, FileTransfer
from wxApi import Panels, Dialogs, DataViews, Toolbars
from wxApi import Transformations as WxTransformations
from wxApi.res import IconSet16
from dbApi import SQLdb, Tools as dbTools

from pprint import pprint


class DatabaseTableBase(object):
    def __init__(self, db_table, form=None, portlet_parent=None):
        self.db_table = db_table
        self.db_object = db_table.db_object
        self.form = form
        self.portlet_parent = portlet_parent
        self.toolbar_parent = None
        self.parent_form = None
        
        self.primary_key = None
        self.filter = None
        
        self.ErrorDialog = Dialogs.Error(parent=self.portlet_parent)
        self.HelpDialog = Dialogs.Help(parent=self.portlet_parent)
        
        
    # Callbacks ---------------------------------------------------------------
    def on_row_activate(self, content_dic=None):
        self.primary_key = content_dic[self.primary_key_column]
        self.edit()


    def on_cursor_changed(self, content_dic=None):
        self.primary_key = content_dic[self.primary_key_column]
        
        
    # Actions -----------------------------------------------------------------
    def new(self, *args, **kwargs):
        if self.form == None:
            print 'no form defined!'
            return
        
        try:
            self.primary_key = None
            form_instance = self.form(parent=self.portlet_parent, remote_parent=self)
            form_instance.populate()
        except Exception, inst:
            self.ErrorDialog.show('Fehler', inst, message='Beim öffnen des Formulars ist ein Fehler aufgetreten!')
            
            
    def edit(self, *args, **kwargs):
        if self.form == None:
            print 'no form defined!'
            return

        form_instance = self.form(parent=self.portlet_parent, remote_parent=self)
        form_instance.populate()


    def delete(self, *args, **kwargs):
        if self.primary_key <> None:
            dialog = wx.MessageDialog(None, u'Soll dieser Datensatz wirklich gelöscht werden?', 'Frage', 
                                    wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            answer = dialog.ShowModal()
            if answer == wx.ID_YES:
                pk_column = self.db_table.get_primary_key_columns()[0]
                self.db_table.delete(where='%s = %s' % (pk_column, self.primary_key))
                self.populate()
                
                
    def initialize(self, definition_lod=None):
        ''' Initializes a treeview as table or tree. The definition_lod
            will be merged with the attributes_lod, thus the attributes_lod
            can be already contained in the definition_lod if desired!

            definition_lod = [{'column_name': 'id',

                               'column_label': 'Primärschlüssel',
                               'column_number': 0,

                               'visible': True,
                               'editable': True,
                               'sortable': True,
                               'resizeable': True,
                               'reorderable': True}]

           attributes_lod = [{'column_name': 'id'

                              'data_type': 'bigint'
                              'character_maximum_length': = 20
                              'numeric_precision' = 2
                              'numeric_scale' = ?
                              'is_nullable' = True}]'''

        self.definition_lod = definition_lod
        self.attributes_lod = self.db_table.attributes
        
        result = WxTransformations.search_lod(self.attributes_lod, 'is_primary_key', True)
        if result <> None: 
            self.primary_key_column = result['column_name']
            
    
    def populate(self, content_lod=None):
#        if self.parent_form <> None: 
#            if self.parent_form.primary_key <> None:
#                # This populates a referenced table (on a parent form)
#                attributes_lod = self.db_table.attributes
#                primary_key_column = self.primary_key_column
#                referenced_table_name = self.parent_form.db_table.name
#                
#                self.foreign_key_column_name = \
#                    self.db_table.get_foreign_key_column_name(attributes_lod, 
#                                                              primary_key_column, 
#                                                              referenced_table_name)
#                    
#                self.content_lod = self.db_table.select(where='%s = %i' % (self.foreign_key_column_name, self.parent_form.primary_key))
#            else:
#                # This clears the table if parent form has no primary_key (f.e. if a new dataset is created!
#                self.content_lod = []
#        else:
        if self.filter == None:
            self.content_lod = self.db_table.get_content()
        elif self.filter == False:
            return
        else:
            self.content_lod = self.db_table.select(where=self.filter)
        # Before populating, check if there are any substitutions from referenced tables
        self.check_column_substitutions()
        
        # Check, if the Table object is still alive. If deleted, just go on.
        attr_list = dir(self.Table)
        if 'populate' in attr_list: #, type(attr_list)
            self.Table.populate(self.content_lod)
        
        # Do callbacks for the population of higher-level widgets.
        for definition_dic in self.definition_lod:
            if definition_dic.has_key('populate_function'):
                definition_dic['populate_function'](definition_dic)
                
                
    def populate_portlet(self):
        self.Table = DataViews.Tree(self.portlet_parent)
        sizer = self.portlet_parent.GetSizer()
        sizer.Add(self.Table, 0, wx.ALL|wx.EXPAND)
        
        self.Table.initialize(definition_lod=self.definition_lod, attributes_lod=self.attributes_lod)
        self.Table.set_row_activate_function(self.on_row_activate)
        self.Table.set_cursor_change_function(self.on_cursor_changed)
        
        # Just populate immideately if this is not a child-table of a form!
        if self.parent_form == None:
            self.populate()
            
        self.Table.Show()
        sizer.Layout()
        return self.Table
        
        
    def add_filter(self, filter_name=None, filter_function=None):
        self.filter_lod.append({'filter_name': filter_name, 'filter_function': filter_function})


    def set_filter(self, filter_name=None):
        pass
        
        
    def check_column_substitutions(self):
        ''' Search for one to one relationships in that table and if any there,
            call the do_column_substitutions function and replace them with content. ''' 
        
        for column_dic in self.definition_lod:
            if column_dic.has_key('populate_from'):
                populate_from = column_dic['populate_from']
                if column_dic.has_key('column_name'):
                    column_name = column_dic['column_name']
                    if column_dic.has_key('referenced_table_name'):
                        referenced_table_name = column_dic['referenced_table_name']
                        if column_dic.has_key('referenced_column_name'):
                            referenced_column_name = column_dic['referenced_column_name']                                        
                            mask = column_dic.get('mask')
                            self.do_column_substitutions(column_name, populate_from, mask, referenced_table_name, referenced_column_name)
        
        
    def do_column_substitutions(self, column_name, populate_from, mask, referenced_table_name, referenced_column_name):
        ''' Substitute foreign keys with content from the foreign tables. '''
        
        for content_dic in self.content_lod:
            substitute_dic = {}
            foreign_key = content_dic[column_name]
            if foreign_key in [None, 'NULL']:
                continue
            referenced_table_object = SQLdb.table(self.db_object, referenced_table_name)
            substitute_lod = referenced_table_object.select(column_list=populate_from, where='%s = %i' % (referenced_column_name, foreign_key))
            if mask == None:
                mask = '%(' +'%s' % populate_from[0] + ')s'
            content_dic[column_name] = mask % substitute_lod[0]

            
    
class SubTable(DatabaseTableBase):
    def __init__(self, db_table, form=None, portlet_parent=None, parent_form=None, editable=True):
        DatabaseTableBase.__init__(self, db_table, form, portlet_parent)
        
        self.editable = editable
        self.parent_form = parent_form
        
        self.sizer = wx.FlexGridSizer(1, 4, 0, 0)
        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableRow(0)
        self.sizer.SetFlexibleDirection( wx.BOTH )
        self.sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.portlet_parent.SetSizer(self.sizer)

        
    def on_add_clicked(self, event=None):
        self.new()
        print 'add'
    
    
    def on_edit_clicked(self, event=None):
        self.edit()
        print 'edit'
    
    
    def on_delete_clicked(self, event=None):
        self.delete()
        print 'delete'
        
        
    def populate_portlet(self):
        super(SubTable, self).populate_portlet()
        self.sizer_buttons = wx.BoxSizer( wx.VERTICAL )
        
        self.button_add = wx.Button( self.portlet_parent, wx.ID_ANY, u"Hinzufügen", wx.DefaultPosition, wx.DefaultSize, 0 )       
        self.sizer_buttons.Add(self.button_add, 0, wx.ALL, 5 )
        self.button_add.Bind(wx.EVT_BUTTON, self.on_add_clicked)
        
        if self.editable == True:
            self.button_edit = wx.Button( self.portlet_parent, wx.ID_ANY, u"Bearbeiten", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.sizer_buttons.Add(self.button_edit, 0, wx.ALL, 5 )
            self.button_edit.Bind(wx.EVT_BUTTON, self.on_edit_clicked)
        
        self.button_delete = wx.Button( self.portlet_parent, wx.ID_ANY, u"Entfernen", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.sizer_buttons.Add(self.button_delete, 0, wx.ALL, 5 )
        self.button_delete.Bind(wx.EVT_BUTTON, self.on_delete_clicked)
        
        self.sizer.Add( self.sizer_buttons, 1, wx.EXPAND, 5 )
        self.portlet_parent.Layout()
        
        if self.parent_form <> None:
            if self.parent_form.primary_key <> None:
                self.populate()
            else:
                self.button_add.Enable(False)
                self.button_delete.Enable(False)
                if self.editable == True:
                    self.button_edit.Enable(False)
        else:
            self.populate()
        
        
        
class FormTable(DatabaseTableBase):
    ID_NEW = 101
    ID_EDIT = 102
    ID_DELETE = 103
    
    ID_PRINT = 201
    
    ID_PREFERENCES = 401
    ID_HELP = 402
    
    
    def __init__(self, db_table, form=None, \
                 toolbar_parent=None, portlet_parent=None, \
                 help_path=None):
        
        ''' db_object is the current opened database object.
            toolbar_parent is an aui toolbar, which has to be populated from here.
            portlet_parent is the underlying parent which contains this widget.
            
            form is a form class, that creates an object here to edit datasets.
            db_table is an instance of a sql_table.
            help_path is the path to the helpfile opened if help pressed. '''
        
        DatabaseTableBase.__init__(self, db_table, form, portlet_parent)
        
        self.toolbar_parent = toolbar_parent
        self.help_path = help_path
        
        # TODO: remove this sheenanigan asap!
        self.parent_form = None
        
    
    # Callbacks ---------------------------------------------------------------
    def on_cursor_changed(self, content_dic=None):
        # First, call the overwritten method to determine primary key.
        super(FormTable, self).on_cursor_changed(content_dic)
        
        if self.toolbar_parent <> None:
            if str(self.primary_key).lower() == 'root':
                self.toolbar_parent.EnableTool(self.ID_EDIT, False)
                self.toolbar_parent.EnableTool(self.ID_DELETE, False)
            else:
                self.toolbar_parent.EnableTool(self.ID_EDIT, True)
                self.toolbar_parent.EnableTool(self.ID_DELETE, True)
            self.toolbar_parent.Realize()
            

    def on_print(self, event=None):
        print "print"
        
    
    def on_export(self, event=None):
        print "export"
        
        
    def on_preferences(self, event=None):
        toplevel_frame = self.portlet_parent.GetTopLevelParent()
        self.frame_preferences = Dialogs.FormTablePreferences(parent=toplevel_frame, title='Einstellungen')
        self.frame_preferences.ShowModal()
        
        
    def on_help(self, event=None):
        if self.help_path <> None:
            self.HTMLhelp.show(self.help_path)
    
                
    def update(self):
        self.button_new.set_sensitive(1)
        self.button_delete.set_sensitive(0)
        self.button_edit.set_sensitive(0)
        
        self.populate()


    def populate_toolbar(self):
        self.toolbar_parent.SetToolBitmapSize(wx.Size(22, 22))
        
        if self.form <> None:
            self.toolbar_parent.AddTool(self.ID_NEW,     "Neu",        IconSet16.getfilenew_16Bitmap())
            self.toolbar_parent.Bind(wx.EVT_TOOL, self.new, id=self.ID_NEW)
    
            self.toolbar_parent.AddTool(self.ID_EDIT,    "Bearbeiten", IconSet16.getedit_16Bitmap())
            self.toolbar_parent.Bind(wx.EVT_TOOL, self.edit, id=self.ID_EDIT)
    
            self.toolbar_parent.AddTool(self.ID_DELETE, u"Löschen",    IconSet16.getdelete_16Bitmap())
            self.toolbar_parent.Bind(wx.EVT_TOOL, self.delete, id=self.ID_DELETE)
    
            self.toolbar_parent.AddSeparator()
        
        self.toolbar_parent.AddTool(self.ID_PRINT, "Drucken",          IconSet16.getprint_16Bitmap())
        self.toolbar_parent.Bind(wx.EVT_TOOL, self.on_print, id=self.ID_PRINT)
        
        #if filter == True:
        self.toolbar_parent.AddSeparator()
        combobox_filter = wx.ComboBox(
            parent=self.toolbar_parent, id=-1, choices=['<alle>'],
            size=(150,-1), style=wx.CB_DROPDOWN)
        self.toolbar_parent.AddControl(combobox_filter)
        
        #if search == True:
        self.toolbar_parent.AddSeparator() 
        entry_search = wx.SearchCtrl(parent=self.toolbar_parent, id=-1)
        self.toolbar_parent.AddControl(entry_search) 
        
        #if preferences == True or help == True:
        self.toolbar_parent.AddSeparator()
        
        #if preferences == True:
        self.toolbar_parent.AddTool(self.ID_PREFERENCES, "Einstellungen", IconSet16.getpreferences_16Bitmap())
        self.toolbar_parent.Bind(wx.EVT_TOOL, self.on_preferences, id=self.ID_PREFERENCES)
        
        if self.help_path <> None:
            self.toolbar_parent.AddLabelTool(self.ID_HELP, label="Hilfe", bitmap=IconSet16.gethelp_16Bitmap())
            self.toolbar_parent.Bind(wx.EVT_TOOL, self.on_help, id=self.ID_HELP)
        
        self.toolbar_parent.Realize()
    
    # This has to come back here!
    # def add_filter(self, filter_name=None, filter_function=None):
        # self.filter_lod.append({'filter_name': filter_name, 'filter_function': filter_function})


    # def set_filter(self, filter_name=None):
        # pass
        #print 'set filter to:', filter_name
        
    

# Form frames ------------------------------------------------------------------
class SearchFrame(wx.Frame):
    ID_OK = 101
    
    def __init__(self, db_table,
                       parent,
                       icon_path=None,
                       title='Suche',
                       remote_parent=None):
        
        ''' This is a database table search form '''
        
        self.db_table = db_table
        self.parent = parent
        self.icon_path = icon_path
        self.title = title
        self.remote_parent = remote_parent
        
        wx.Frame.__init__(self, self.parent, wx.ID_ANY, self.title, size=(640, 480))
        if icon_path <> None:
            self.SetIcon(wx.Icon(self.icon_path, wx.BITMAP_TYPE_ICO))
        
        self.Bind(wx.EVT_CLOSE, self.on_close)
        
        self.aui_manager = wx.aui.AuiManager(self)
        
        self.create_toolbar()
        self.aui_manager.AddPane(self.toolbar_standard, wx.aui.AuiPaneInfo().
                         Name("toolbar_standard").Caption("Standard").
                         ToolbarPane().Top().Resizable().
                         LeftDockable(False).RightDockable(False))
        
        self.panel = wx.Panel(self, wx.ID_ANY, size=(300, 200))
        self.sizer = wx.FlexGridSizer(1, 4, 0, 0)
        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableRow(0)
        self.sizer.SetFlexibleDirection( wx.BOTH )
        self.sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        self.panel.SetSizer(self.sizer)
        self.aui_manager.AddPane(self.panel, wx.aui.AuiPaneInfo().CaptionVisible(False).
                                 Name("panel_main").TopDockable(False).
                                 Center().Layer(1).CloseButton(False))
        self.populate_table()
        self.aui_manager.Update()
        self.Show()
        
        self.db_object = self.db_table.db_object
        
        self.error_dialog = Dialogs.Error(self)
        
        
    def on_ok(self, event=None):
        self.edit()
        
        
    def on_close(self, event=None):
        del(self.toolbar_standard)
        self.Destroy()
        
        
    def create_toolbar(self, dataset=True, report=True, help=True):
        self.toolbar_standard = wx.aui.AuiToolBar(self, id=wx.ID_ANY) 
        
        self.toolbar_standard.AddTool(self.ID_OK, "Ok", IconSet16.getok_16Bitmap())
        self.toolbar_standard.Bind(wx.EVT_TOOL, self.on_ok, id=self.ID_OK)
        
        self.toolbar_standard.AddSeparator()
        
        entry_search = wx.SearchCtrl(parent=self.toolbar_standard, id=wx.ID_ANY)
        self.toolbar_standard.AddControl(entry_search) 
        
        self.toolbar_standard.AddSeparator()
        
        self.toolbar_standard.AddTool(wx.ID_ANY, "Drucken", IconSet16.getprint_16Bitmap())
        
    
    def populate_table(self):
        self.table = DatabaseTableBase(self.db_table, portlet_parent=self.panel)
        self.db_table.attributes = self.db_table.get_attributes()
        
        self.table.initialize(self.definition)
        self.table.populate_portlet()
        
        self.table.edit = self.edit
        
        
    def edit(self):
        self.add_dataset(self.table.primary_key)
        self.remote_parent.populate()
        self.Close()
        
        
    def populate(self):
        pass
        
        
        
class FormFrame(wx.Frame):
    ID_SAVE = 101
    ID_DELETE = 102
    ID_PRINT = 103
    
    ID_PREFERENCES = 201
    ID_HELP = 202
    
    def __init__(self, parent=None,
                       icon_path=None,
                       title='',
                       xrc_path=None,
                       panel_name=None,
                       help_path=None,
                       remote_parent=None):
        
        ''' db_table is the the table in which this Form writes the data. The remote_parent
            is triggered on save and close, so that the parent widget can be updated. parent
            is simply the wxWidgets-Parent, usually a Frame. title is the Frame-title, 
            panel_name is the name of the panel which is loaded from the file behind xrc_path.
            The help-path enables online help, if given. '''
        
        self.parent = parent 
        self.title = title
        self.panel_name = panel_name
        self.icon_path = icon_path
        self.xrc_path = xrc_path
        self.help_path = help_path
        self.remote_parent = remote_parent
        
        # This lists are made to get portlets going.
        self.save_function_list = []
        self.delete_function_list = []
        
        wx.Frame.__init__(self, self.parent, wx.ID_ANY, self.title) #, size=(640,480))
        if icon_path <> None:
            self.SetIcon(wx.Icon(self.icon_path, wx.BITMAP_TYPE_ICO))
        
        self.Bind(wx.EVT_CLOSE, self.on_close)
        
        self.primary_key = None
        if self.remote_parent.primary_key <> None:
            self.primary_key = self.remote_parent.primary_key
        
        self.aui_manager = wx.aui.AuiManager(self)
        
        self.create_toolbar()
        self.form = DataViews.Form(self, self.xrc_path, self.panel_name)
        
        self.aui_manager.AddPane(self.toolbar_standard, wx.aui.AuiPaneInfo().
                         Name("toolbar_standard").Caption("Standard").
                         ToolbarPane().Top().Resizable().
                         LeftDockable(False).RightDockable(False))
        self.aui_manager.AddPane(self.form, wx.aui.AuiPaneInfo().CaptionVisible(False).
                                 Name("panel_main").TopDockable(False).
                                 Center().Layer(1).CloseButton(False))
        self.aui_manager.Update()
        self.Show()
        self.Centre()
        
        self.db_table = remote_parent.db_table
        self.db_object = self.db_table.db_object
        
        self.error_dialog = Dialogs.Error(self)
        
        
    def on_close(self, event=None):
        del(self.toolbar_standard)
        self.Destroy()
        
        
    def on_save(self, event=None):
        form_content = self.form.get_content()
        pk_column = self.db_table.get_primary_key_columns()[0]
        
        try:
            if self.primary_key <> None:
                form_content[pk_column] = self.primary_key
                self.db_table.update(form_content, where='%s = %s' % (pk_column, self.primary_key))
            else:
                self.primary_key = self.db_table.insert(key_column=pk_column, content=form_content)
        except Exception, inst:
            self.error_dialog.show(instance=inst, message='Beim speichern dieses Datensatzes ist ein Fehler aufgetreten!')
        
        self.remote_parent.populate()
        for function in self.save_function_list:
            function(self.primary_key)
        self.on_close()
        
        
    def on_delete(self, event=None):
        print 'delete formular'
        for function in self.delete_function_list:
            function(self.primary_key)
        
        
    def on_print(self, event=None):
        print 'print formular'
        
        
    def on_preferences(self, event=None):
        self.frame_preferences = Dialogs.FormTablePreferences(parent=self, title='Einstellungen')
        self.frame_preferences.ShowModal()
        
        
    def on_help(self, event=None):
        print 'help'
        
        
    def initialize(self, definition_lod=None, attributes_lod=None, portlets_lod=None):
        self.definition_lod = definition_lod
        self.attributes_lod = attributes_lod
        
        self.form.initialize(definition_lod=self.definition_lod, 
                             attributes_lod=self.attributes_lod)
        self.definition_lod = self.form.definition_lod

        
    def populate(self):
        if self.primary_key <> None:
            pk_column = self.db_table.get_primary_key_columns()[0]
            content_lod = self.db_table.select(where='%s = %s' % (pk_column, self.primary_key))
            content_dict = content_lod[0]
            self.form.populate(content_dict)
            
        # This populates the dropdown of comboboxes.
        definition_lod = self.form.definition_lod
        for dic in definition_lod:
            populate_from = dic.get('populate_from')
            mask = dic.get('mask')
            referenced_table_name = dic.get('referenced_table_name')
            referenced_column_name = dic.get('referenced_column_name')
            widget_object = dic.get('widget_object')
            column_name = dic.get('column_name')
            on_populate = dic.get('on_populate')
            
            if on_populate <> None:
                on_populate(dic)
                
            if populate_from == None:
                continue
            if mask == None:
                mask = '%(' +'%s' % populate_from[0] + ')s'
                
            populate_from.append(referenced_column_name)
            referenced_table_object = SQLdb.table(self.db_object, referenced_table_name)
            result = referenced_table_object.select(column_list=populate_from)
            item_list = []
            for item in result:
                widget_object.Append(mask % item, item.get(referenced_column_name))
            
            if self.primary_key <> None:
                # Overwrite crap in combobox if feeded from foreign table!
                foreign_key = content_dict.get(column_name)
                if foreign_key <> None:
                    result = referenced_table_object.select(column_list=populate_from, where='%s = %s' % (referenced_column_name, foreign_key))
                    result_dict = result[0]
                    widget_object.SetStringSelection(mask % result_dict)
    
    
    def create_toolbar(self, dataset=True, report=True, help=True):
        self.toolbar_standard = wx.aui.AuiToolBar(self, id=wx.ID_ANY) 
        
        self.toolbar_standard.AddTool(self.ID_SAVE, "Speichern", IconSet16.getfilesave_16Bitmap())
        self.toolbar_standard.Bind(wx.EVT_TOOL, self.on_save, id=self.ID_SAVE)
        
        self.toolbar_standard.AddTool(self.ID_DELETE, "Löschen", IconSet16.getdelete_16Bitmap())
        self.toolbar_standard.Bind(wx.EVT_TOOL, self.on_delete, id=self.ID_DELETE)
        
        self.toolbar_standard.AddTool(self.ID_PRINT, "Drucken", IconSet16.getprint_16Bitmap())
        self.toolbar_standard.Bind(wx.EVT_TOOL, self.on_print, id=self.ID_PRINT)
        
        # If no primary key is there, just deactivate delete and print!
        if self.primary_key == None:
            self.toolbar_standard.EnableTool(self.ID_DELETE, False)
            self.toolbar_standard.EnableTool(self.ID_PRINT,  False)
            
        self.toolbar_standard.AddSeparator()
        self.toolbar_standard.AddTool(self.ID_PREFERENCES, "Einstellungen", IconSet16.getpreferences_16Bitmap())
        self.toolbar_standard.Bind(wx.EVT_TOOL, self.on_preferences, id=self.ID_PREFERENCES)
        
        if self.help_path <> None:
            self.toolbar_standard.AddTool(self.ID_HELP, "Hilfe", IconSet16.gethelp_16Bitmap())
            self.toolbar_standard.Bind(wx.EVT_TOOL, self.on_help, id=self.ID_HELP)
        
        
    def get_widget(self, widget_name):
        widget = self.form.get_widget(widget_name)
        return widget
    
    
    def add_save_function(self, function):
        self.save_function_list.append(function)

    
    def add_delete_function(self, function):
        self.delete_function_list.append(function)
        
        
        
        
        