# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wxDataViews module.
# by Mark Muzenhardt, published under LGPL license.
#===============================================================================

import wx, wx.aui

from misc import FileSystem, HelpFile, FileTransfer
from wxApi import Panels, Dialogs, DataViews, Toolbars
from wxApi import Transformations as WxTransformations
from wxApi.res import IconSet16
from dbApi import SQLdb, Tools as dbTools
from ContentDefinitionBase import TableContentBase
from config import *

from pprint import pprint


# Table widgets ----------------------------------------------------------------
class DatabaseTableBase(TableContentBase):
    def __init__(self, db_table, form=None, portlet_parent=None, editable=True, permissions={}):
        self.db_table = db_table
        self.db_object = db_table.db_object
        self.form = form
        self.portlet_parent = portlet_parent
        self.editable = editable
        self.fetch = None
        
        if permissions <> None:
            self.permissions = permissions.get('table')
            self.form_permissions = permissions.get('form')
            self.userdata = permissions.get('userdata')
        else:
            self.permissions = {}
            self.form_permissions = {}
            self.userdata = {}
        
        self.toolbar_parent = None
        self.parent_form = None
        
        self.primary_key = None
        self.filter = None
        self.search_columns = []
        self.search_string = ''
        self.deleted_filter = ''
        
        self.delete_function_list = []
        self.selected_row_content = None
        
        self.ErrorDialog = Dialogs.Error(parent=self.portlet_parent)
        self.HelpDialog = Dialogs.Help(parent=self.portlet_parent)
        
        self.row_right_click_function = None
        #TODO: This is gay, please subclass the Table (or what do I fear?
        #self.Table = DataViews.Tree(self.portlet_parent)
        
        
    # Callbacks ---------------------------------------------------------------
    def on_row_activate(self, content_dic=None):
        self.primary_key = content_dic[self.primary_key_column]
        if self.editable == True:
            self.edit()


    def on_cursor_changed(self, content_dic=None):
        self.selected_row_content = content_dic
        self.primary_key = content_dic[self.primary_key_column]
        #print self.selected_row_content
        
        
    # Actions -----------------------------------------------------------------
    def new(self, *args, **kwargs):
        if self.form == None:
            print 'no form defined!'
            return
        
        try:
            self.primary_key = None
            # print self.form
            form_instance = self.form(parent=self.portlet_parent, remote_parent=self, permissions=self.form_permissions)
            form_instance.populate()
        except Exception, inst:
            self.ErrorDialog.show('Fehler', inst, message='Beim öffnen des Formulars ist ein Fehler aufgetreten!')
            
            
    def edit(self, *args, **kwargs):
        if self.form == None:
            print 'no form defined!'
            return
        
        form_instance = self.form(parent=self.portlet_parent, remote_parent=self, permissions=self.form_permissions)
        form_instance.populate()
        
        
    def delete(self, *args, **kwargs):
        if self.primary_key <> None:
            dialog = wx.MessageDialog(None, u'Soll dieser Datensatz wirklich gelöscht werden?', 'Frage', 
                                    wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            answer = dialog.ShowModal()
            if answer == wx.ID_YES:
                pk_column = self.db_table.get_primary_key_columns()[0]
                
                try:
                    self.db_table.delete(where='%s = %s' % (pk_column, self.primary_key))
                    for delete_function in self.delete_function_list:
                        delete_function(self.primary_key)
                    self.populate()
                except Exception, inst:
                    self.ErrorDialog.show(title='Fehler', instance=inst, message=u'Fehler beim Löschen des Datensatzes!')

        
    def add_delete_function(self, delete_function):
        self.delete_function_list.append(delete_function)
        
              
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
            
    
    def build_where_clause(self):
        if self.filter <> None:
            clause = self.filter
            if self.search_columns <> []:
                clause += ' AND ('
        else:
            clause = ''
        for column in self.search_columns:
            clause += column + " LIKE '%" + self.search_string + "%' OR "
        if self.search_columns <> []:
            clause = clause[:len(clause)-4]
        if self.filter <> None and self.search_columns <> []:
            clause += ')'
        if self.deleted_filter <> '':
            if clause <> '':
                clause = '(%s) AND %s' % (clause, self.deleted_filter)
            else:
                clause = self.deleted_filter
        return clause
    
        
    def populate(self, content_lod=None):
        if content_lod == None:
            if self.filter == None and self.search_string == None:
                self.content_lod = self.db_table.get_content(order_by=self.primary_key_column + ' DESC', fetch=self.fetch)
            elif self.filter == False:
                return
            else:
                clause = self.build_where_clause()
                self.content_lod = self.db_table.select(order_by=self.primary_key_column + ' DESC', where=clause, fetch=self.fetch)
        else:
            self.content_lod = content_lod
            
        # Before populating, check if there are any substitutions from referenced tables
        self.check_column_substitutions()
        
        # Check, if the Table object is still alive. If deleted, just go on.
        attr_list = dir(self.Table)
        if 'populate' in attr_list:
            self.Table.populate(self.content_lod)
        
        # Do callbacks for the population of higher-level widgets.
        for definition_dic in self.definition_lod:
            if definition_dic.has_key('populate_function'):
                definition_dic['populate_function'](definition_dic)
                
                
    def create(self):
        # Just creates a panel to draw the Table on, that buttons or else can be 
        # attached near the Table!
        self.main_panel = wx.Panel(self.portlet_parent)
        sizer = self.portlet_parent.GetSizer()
        sizer.Add(self.main_panel, 0, wx.ALL|wx.EXPAND)
        
        self.main_sizer = wx.FlexGridSizer(1, 1, 0, 0)
        self.main_sizer.AddGrowableCol(0)
        self.main_sizer.AddGrowableRow(0)
        self.main_sizer.SetFlexibleDirection( wx.BOTH )
        self.main_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        self.main_panel.SetSizer(self.main_sizer)
        
        self.Table = DataViews.Tree(self.main_panel)
        self.Table.row_right_click_function = self.row_right_click_function
        
        self.main_sizer.Add(self.Table, 0, wx.ALL|wx.EXPAND)        
        
        self.Table.initialize(definition_lod=self.definition_lod, attributes_lod=self.attributes_lod)
        self.Table.set_row_activate_function(self.on_row_activate)
        self.Table.set_cursor_change_function(self.on_cursor_changed)
        
        # Just populate immideately if this is not a child-table of a form!
        if self.parent_form == None:
            self.populate()

        self.Table.Show()       
        return self.main_panel
        
        
    def add_filter(self, filter_name=None, filter_function=None):
        self.filter_lod.append({'filter_name': filter_name, 'filter_function': filter_function})

        
    def set_filter(self, filter_name=None):
        pass
        
        
    def set_search_columns(self, search_columns):
        self.search_columns = search_columns
        

    def set_search_string(self, search_string):
        self.search_string = search_string
        self.populate()
        
        
        
class SubTable(DatabaseTableBase):
    def __init__(self, db_table, form=None, portlet_parent=None, parent_form=None, editable=True, permissions={}):
        DatabaseTableBase.__init__(self, db_table, form, portlet_parent, editable, permissions)
        
        self.editable = editable
        self.parent_form = parent_form
        self.permissions = permissions
        
        self.sizer = wx.FlexGridSizer(1, 4, 0, 0)
        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableRow(0)
        self.sizer.SetFlexibleDirection( wx.BOTH )
        self.sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.portlet_parent.SetSizer(self.sizer)

        
    def on_add_clicked(self, event=None):
        self.new()
    
    
    def on_edit_clicked(self, event=None):
        self.edit()
    
    
    def on_delete_clicked(self, event=None):
        self.delete()
        
        
    def create(self):
        super(SubTable, self).create()
        self.sizer_buttons = wx.BoxSizer( wx.VERTICAL )
        
        if self.permissions == None:
            self.permissions = {}
            
        if self.permissions.get('new') <> False:
            self.button_add = wx.Button( self.portlet_parent, wx.ID_ANY, u"Hinzufügen", wx.DefaultPosition, wx.DefaultSize, 0 )       
            self.sizer_buttons.Add(self.button_add, 0, wx.ALL, 5 )
            self.button_add.Bind(wx.EVT_BUTTON, self.on_add_clicked)
            
        if self.editable == True and self.permissions.get('edit') <> False:
            self.button_edit = wx.Button( self.portlet_parent, wx.ID_ANY, u"Bearbeiten", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.sizer_buttons.Add(self.button_edit, 0, wx.ALL, 5 )
            self.button_edit.Bind(wx.EVT_BUTTON, self.on_edit_clicked)
        
        if self.permissions.get('delete') <> False:
            self.button_delete = wx.Button( self.portlet_parent, wx.ID_ANY, u"Entfernen", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.sizer_buttons.Add(self.button_delete, 0, wx.ALL, 5 )
            self.button_delete.Bind(wx.EVT_BUTTON, self.on_delete_clicked)
        
        self.sizer.Add( self.sizer_buttons, 1, wx.EXPAND, 5 )
        self.portlet_parent.Layout()
        
        if self.parent_form <> None:
            if self.parent_form.primary_key <> None:
                self.populate()
            else:
                if self.permissions.get('new') <> False:
                    self.button_add.Enable(False)
                if self.permissions.get('delete') <> False:
                    self.button_delete.Enable(False)
                if self.editable == True and self.permissions.get('edit') <> False:
                    self.button_edit.Enable(False)
        else:
            self.populate()
        
        
        
class FormTable(DatabaseTableBase):
    #TODO: Search should be self.search (string)
    #TODO: Filter should be self.filter = {'text': 'Becker', 'sql': 'name=Becker'}
    #TODO: When delete just sets the delete column, there has to be a function called "set_delete_column"
    #TODO: self.where_clause should be fitted together from self.search AND self.filter[sql] AND self.delete_column NOT 1 or so...
        
    ID_NEW = 101
    ID_EDIT = 102
    ID_DELETE = 103
    ID_PRINT = 201
    ID_EXPORT_TABLE = 202
    #ID_PREFERENCES = 401
    ID_HELP = 402
    
    
    def __init__(self, db_table, form=None, \
                 toolbar_parent=None, portlet_parent=None, \
                 help_path=None, permissions={}, \
                 excel_class=None, print_class=None):
        
        ''' db_object is the current opened database object.
            toolbar_parent is an aui toolbar, which has to be populated from here.
            portlet_parent is the underlying parent which contains this widget.
            
            form is a form class, that creates an object here to edit datasets.
            db_table is an instance of a sql_table.
            help_path is the path to the helpfile opened if help pressed. '''
        
        DatabaseTableBase.__init__(self, db_table, form, portlet_parent, permissions=permissions)
        
        toplevel_frame = self.portlet_parent.GetTopLevelParent()
        self.frame_preferences = FormTablePreferences(parent=toplevel_frame, title='Einstellungen', remote_parent=self)
        
        self.toolbar_parent = toolbar_parent
        self.help_path = help_path
        
        #print 'wxPermi:', permissions #, form
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
        # TODO: Good point: content_lod is always ok to do print!
        #pprint(self.content_lod)
        
    
    def on_search(self, event=None):
        self.set_search_string(self.entry_search.GetValue())
        
        
    def on_export(self, event=None):
        print "export"
        # TODO: Good point: content_lod is always ok to do export!
        #pprint(self.content_lod)
        
        
    def on_preferences(self, event=None):
        #self.frame_preferences = FormTablePreferences(parent=toplevel_frame, title='Einstellungen', remote_parent=self)
        self.frame_preferences.ShowModal()
        
        
    def on_help(self, event=None):
        if self.help_path <> None:
            self.HTMLhelp.show(self.help_path)
    
    
    def on_combobox_filter_changed(self, event=None):
        selection = self.combobox_filter.GetSelection()
        if selection == 0:
            self.fetch = None
        if selection == 1:
            self.fetch = 100
        if selection == 2:
            self.fetch = 500
        if selection == 3:
            self.fetch = 1000
        self.Table.SetFocus()
        self.populate()
        
        
    def update(self):
        self.button_new.set_sensitive(1)
        self.button_delete.set_sensitive(0)
        self.button_edit.set_sensitive(0)
        
        self.populate()


    def create_toolbar(self):
        self.toolbar_parent.SetToolBitmapSize(wx.Size(22, 22))
        
        if self.permissions == None:
            self.permissions = {}
        
        if self.form <> None:
            if self.permissions.get('new') <> False:
                self.toolbar_parent.AddTool(self.ID_NEW,     "Neu",        IconSet16.getfilenew_16Bitmap(), 'neu')
                self.toolbar_parent.Bind(wx.EVT_TOOL, self.new, id=self.ID_NEW)
                
            if self.permissions.get('edit') <> False:    
                self.toolbar_parent.AddTool(self.ID_EDIT,    "Bearbeiten", IconSet16.getedit_16Bitmap(), 'bearbeiten')
                self.toolbar_parent.Bind(wx.EVT_TOOL, self.edit, id=self.ID_EDIT)
                
            if self.permissions.get('delete') <> False:    
                self.toolbar_parent.AddTool(self.ID_DELETE, u"Löschen",    IconSet16.getdelete_16Bitmap(), u'löschen')
                self.toolbar_parent.Bind(wx.EVT_TOOL, self.delete, id=self.ID_DELETE)
                
        if (self.permissions.get('new') or \
            self.permissions.get('edit') or \
            self.permissions.get('delete')) <> False:
            self.toolbar_parent.AddSeparator()
        
#        if self.permissions.get('print') <> False:
#            self.toolbar_parent.AddTool(self.ID_PRINT, "Drucken",          IconSet16.getprint_16Bitmap(), 'drucken')
#            self.toolbar_parent.Bind(wx.EVT_TOOL, self.on_print, id=self.ID_PRINT)
        
        if self.permissions.get('export') <> False:
            self.toolbar_parent.AddTool(self.ID_EXPORT_TABLE, "Tabelle exportieren", IconSet16.getspreadsheet_16Bitmap(), 'Tabelle exportieren')
            self.toolbar_parent.Bind(wx.EVT_TOOL, self.on_export, id=self.ID_EXPORT_TABLE)
        
        #if search == True:
        if (self.permissions.get('print') or \
            self.permissions.get('export')) <> False:
            self.toolbar_parent.AddSeparator() 
        
        self.entry_search = wx.SearchCtrl(parent=self.toolbar_parent, id=-1)
        self.entry_search.SetDescriptiveText('Volltextsuche')
        self.entry_search.Bind(wx.EVT_TEXT_ENTER, self.on_search)
        self.toolbar_parent.AddControl(self.entry_search) 
        
        #if filter == True:
        self.toolbar_parent.AddSeparator()
        self.combobox_filter = wx.ComboBox(
            parent=self.toolbar_parent, id=-1, choices=['<alle>', 'letzte 100', 'letzte 500', 'letzte 1000'],
            size=(150,-1), style=wx.CB_DROPDOWN)
        self.combobox_filter.SetToolTip(wx.ToolTip('Filter'))
        self.combobox_filter.SetSelection(2)
        self.fetch = 500
        self.combobox_filter.Bind(wx.EVT_COMBOBOX, self.on_combobox_filter_changed)
        self.toolbar_parent.AddControl(self.combobox_filter)
        
        #if preferences == True or help == True:
        #self.toolbar_parent.AddSeparator()
        
        #if preferences == True:
        #self.toolbar_parent.AddTool(self.ID_PREFERENCES, "Einstellungen", IconSet16.getpreferences_16Bitmap())
        #self.toolbar_parent.Bind(wx.EVT_TOOL, self.on_preferences, id=self.ID_PREFERENCES)
        
        #if self.help_path <> None:
        #    self.toolbar_parent.AddLabelTool(self.ID_HELP, label="Hilfe", bitmap=IconSet16.gethelp_16Bitmap())
        #    self.toolbar_parent.Bind(wx.EVT_TOOL, self.on_help, id=self.ID_HELP)
        
        self.toolbar_parent.Realize()
    
    # This has to come back here!
    # def add_filter(self, filter_name=None, filter_function=None):
        # self.filter_lod.append({'filter_name': filter_name, 'filter_function': filter_function})


    # def set_filter(self, filter_name=None):
        # pass
        #print 'set filter to:', filter_name
        
    

class FormTablePreferences(Dialogs.FormTablePreferences):
    def __init__(self, parent, title, remote_parent):
        Dialogs.FormTablePreferences.__init__(self, parent, title)
        
        self.remote_parent = remote_parent
        
        self.panel_export.button_export.Bind(wx.EVT_BUTTON, self.on_export)
        
        
    def on_export(self, event=None):
        content_lod = self.remote_parent.content_lod
        definition_lod = self.remote_parent.definition_lod
        filepath = self.panel_export.filepicker_export.GetPath()
        
        import csv
        
        column_list = content_lod[0].keys() #[]
#        for definition_dict in definition_lod:
#            column_name = definition_dict.get('column_name')
#            column_label = definition_dict.get('column_label')
#            # column_list.append(column_name)
            
        csv_writer = csv.DictWriter(open(filepath, 'wb'), fieldnames=column_list, delimiter=';')
        
        column_dict = {}
        for column_name in column_list:
            column_label = column_name
            for definition_dict in definition_lod:
                if definition_dict.get('column_name') == column_name:
                    column_label = definition_dict.get('column_label')
                    
            column_dict[column_name] = column_label
        csv_writer.writerow(column_dict)
        
        for content_dict in content_lod:
            csv_writer.writerow(content_dict)
        
        
        
# Form frames ------------------------------------------------------------------
class DatabaseFormBase(object):
    def __init__(self, parent=None,
                       icon_path=None,
                       title='',
                       xrc_path=None,
                       panel_name=None,
                       remote_parent=None,
                       permissions={}):
        
        self.parent = parent 
        self.title = title
        self.panel_name = panel_name
        self.icon_path = icon_path
        self.xrc_path = xrc_path
        
        self.remote_parent = remote_parent
        self.permissions = permissions
        
        # This lists are made to get portlets going.
        self.save_function_list = []
        self.delete_function_list = []
        self.populate_function_list = []
        
        self.primary_key = None
        if self.remote_parent.primary_key <> None:
            self.primary_key = self.remote_parent.primary_key
            
        self.db_table = remote_parent.db_table
        self.db_object = self.db_table.db_object
        
        
    def on_save(self, event=None):
        form_content = self.get_content()
        pk_column = self.db_table.get_primary_key_columns()[0]
        
        for definition_dict in self.definition_lod:
            if 'static' in definition_dict:
                form_content[definition_dict['column_name']] = definition_dict.get('static')
                
        try:
            if self.primary_key <> None:
                form_content[pk_column] = self.primary_key
                self.db_table.update(form_content, where='%s = %s' % (pk_column, self.primary_key))
            else:
                self.primary_key = self.db_table.insert(key_column=pk_column, content=form_content)
            
            for function in self.save_function_list:
                function(self.primary_key)
                
            self.remote_parent.populate()
            self.on_close()
        except Exception, inst:
            self.error_dialog.show(instance=inst, message='Beim speichern dieses Datensatzes ist ein Fehler aufgetreten!')
                
        
    def on_delete(self, event=None):
        dialog = wx.MessageDialog(None, u'Soll dieser Datensatz wirklich gelöscht werden?', 'Frage', 
                                    wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        answer = dialog.ShowModal()
        if answer == wx.ID_YES:
            pk_column = self.db_table.get_primary_key_columns()[0]
            try:
                self.db_table.delete(where='%s = %s' % (pk_column, self.primary_key))
                
                for function in self.delete_function_list:
                    function(self.primary_key)
            
                self.remote_parent.populate()
                self.on_close()
            except Exception, inst:
                self.error_dialog.show(instance=inst, message='Beim löschen dieses Datensatzes ist ein Fehler aufgetreten!')
        
        
    def initialize(self, definition_lod=None, attributes_lod=None, portlets_lod=None):
        self.definition_lod = definition_lod
        self.attributes_lod = attributes_lod
        
        self.form.initialize(definition_lod=self.definition_lod, 
                             attributes_lod=self.attributes_lod)
        self.definition_lod = self.form.definition_lod

        
    def populate(self, content_dict=None):
        if content_dict <> None:
            self.form.populate(content_dict)
            
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
            referenced_table_object = dic.get('referenced_table_object')
            if referenced_table_object <> None:
                referenced_column_name = referenced_table_object.get_primary_key_columns()[0]
            #referenced_column_name = dic.get('referenced_column_name')
            widget_object = dic.get('widget_object')
            column_name = dic.get('column_name')
            fill_distinct = dic.get('fill_distinct')
            on_populate = dic.get('on_populate')
            sort_by = dic.get('sort_by')
            
            if self.permissions <> None:
                enable_list = self.permissions.get('enable')
                if type(enable_list) == list:
                    if column_name not in enable_list:
                        if widget_object <> None:
                            widget_object.Enable(False)
            
            if fill_distinct == True:
                result = self.db_table.select(distinct=True, column_list=[column_name], listresult=True)
                for item in result:
                    if item == None:
                        continue
                    widget_object.Append(str(item))
                
            if on_populate <> None:
                on_populate(dic)
                
            if populate_from == None:
                continue
            if mask == None:
                mask = '%(' +'%s' % populate_from[0] + ')s'
            
            if referenced_table_object == None:
                continue
            
            populate_from.append(referenced_column_name)
            result = referenced_table_object.select(column_list=populate_from)
            
            if sort_by <> None:
                result = sorted(result, key=lambda result: result[sort_by])
                
            if widget_object.__class__ ==  wx._controls.ComboBox:
                for item in result:
                    widget_object.Append(mask % item, item.get(referenced_column_name))
            
            if self.primary_key <> None:
                # Overwrite crap in combobox or textctrl if feeded from foreign table!
                foreign_key = content_dict.get(column_name)
                if foreign_key <> None:
                    result = referenced_table_object.select(column_list=populate_from, where='%s = %s' % (referenced_column_name, foreign_key))
                    result_dict = result[0]
                    if widget_object.__class__ ==  wx._controls.ComboBox:
                        widget_object.SetStringSelection(mask % result_dict)
                    if widget_object.__class__ ==  wx._controls.TextCtrl:
                        widget_object.SetValue(mask % result_dict)
                
                
        for function in self.populate_function_list:
            function(self)
            
            
    def get_widget(self, widget_name):
        widget = self.form.get_widget(widget_name)
        return widget
    
    
    def get_content(self, primary_key_column=None):
        form_content = self.form.get_content()
        if primary_key_column <> None:
            form_content[primary_key_column] = self.primary_key
        return form_content
        
    
    def add_save_function(self, function):
        self.save_function_list.append(function)
        
    
    def add_delete_function(self, function):
        self.delete_function_list.append(function)
        
        
    def add_populate_function(self, function):
        self.populate_function_list.append(function)


        
class FormFrame(wx.Frame, DatabaseFormBase):
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
                       remote_parent=None,
                       permissions={}):
        
        ''' db_table is the the table in which this Form writes the data. The remote_parent
            is triggered on save and close, so that it can be updated then. The parent
            is simply the wxWidgets-Parent, usually a Frame. title is the Frame-title, 
            panel_name is the name of the panel which is loaded from the file behind xrc_path.
            The help-path enables online help, if given. '''
        
        self.help_path = help_path
        self.print_function_list = []
        
        DatabaseFormBase.__init__(self, parent, icon_path, title, xrc_path, panel_name, remote_parent, permissions)
        wx.Frame.__init__(self, self.parent, wx.ID_ANY, self.title) #, size=(640,480))
        if icon_path <> None:
            self.SetIcon(wx.Icon(self.icon_path, wx.BITMAP_TYPE_ICO))
        
        self.Bind(wx.EVT_CLOSE, self.on_close)
        
        self.aui_manager = wx.aui.AuiManager(self)
        self.create_toolbar()
        self.form = DataViews.Form(self, self.xrc_path, self.panel_name)
        self.error_dialog = Dialogs.Error(self)
        
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
        
        
    def on_close(self, event=None):
        del(self.toolbar_standard)
        self.Destroy()
        
        
    def on_print(self, event=None):
        #TODO: It would be better if self would be given on_delete and on_save.
        for function in self.print_function_list:
            function(self)
            
        
    def on_preferences(self, event=None):
        self.frame_preferences = FormTablePreferences(parent=self, title='Einstellungen', remote_parent=self)
        self.frame_preferences.ShowModal()
        
        
    def on_help(self, event=None):
        print 'help'
    
    
    def create_toolbar(self, dataset=True, report=True, help=True):
        self.toolbar_standard = wx.aui.AuiToolBar(self, id=wx.ID_ANY) 
        
        if self.permissions == None:
            self.permissions = {}
            
        if self.permissions.get('save') <> False:
            self.toolbar_standard.AddTool(self.ID_SAVE, "Speichern", IconSet16.getfilesave_16Bitmap(), 'speichern')
            self.toolbar_standard.Bind(wx.EVT_TOOL, self.on_save, id=self.ID_SAVE)
        
        if self.permissions.get('delete') <> False:
            self.toolbar_standard.AddTool(self.ID_DELETE, "Löschen", IconSet16.getdelete_16Bitmap(), u'löschen')
            self.toolbar_standard.Bind(wx.EVT_TOOL, self.on_delete, id=self.ID_DELETE)
        
        if self.permissions.get('print') <> False:
            self.toolbar_standard.AddTool(self.ID_PRINT, "Drucken", IconSet16.getprint_16Bitmap(), u'drucken')
            self.toolbar_standard.Bind(wx.EVT_TOOL, self.on_print, id=self.ID_PRINT)
        
        # If no primary key is there, just deactivate delete and print!
        if self.primary_key == None:
            self.toolbar_standard.EnableTool(self.ID_DELETE, False)
            self.toolbar_standard.EnableTool(self.ID_PRINT,  False)
            
        #self.toolbar_standard.AddSeparator()
        #self.toolbar_standard.AddTool(self.ID_PREFERENCES, "Einstellungen", IconSet16.getpreferences_16Bitmap())
        #self.toolbar_standard.Bind(wx.EVT_TOOL, self.on_preferences, id=self.ID_PREFERENCES)
        
        #if self.help_path <> None:
        #    self.toolbar_standard.AddTool(self.ID_HELP, "Hilfe", IconSet16.gethelp_16Bitmap())
        #    self.toolbar_standard.Bind(wx.EVT_TOOL, self.on_help, id=self.ID_HELP)
        
        
    def add_print_function(self, function):
        self.print_function_list.append(function)
        
        

class SubForm(wx.Frame, DatabaseFormBase):
    def __init__(self, parent=None,
                       icon_path=None,
                       title='',
                       xrc_path=None,
                       panel_name=None,
                       remote_parent=None,
                       permissions={}):
        
        DatabaseFormBase.__init__(self, parent, icon_path, title, xrc_path, panel_name, remote_parent, permissions)
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = title, pos = wx.DefaultPosition, size = wx.DefaultSize) #, style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )
        if icon_path <> None:
            self.SetIcon(wx.Icon(self.icon_path, wx.BITMAP_TYPE_ICO))
        
        sizer_main = wx.FlexGridSizer( 2, 1, 0, 0 )
        sizer_main.AddGrowableCol( 0 )
        sizer_main.AddGrowableRow( 0 )
        sizer_main.SetFlexibleDirection( wx.BOTH )
        sizer_main.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.form = DataViews.Form(self, self.xrc_path, self.panel_name)
        sizer_main.Add( self.form, 1, wx.EXPAND |wx.ALL, 5 )
        
        sizer_buttons = wx.BoxSizer( wx.HORIZONTAL )
        sizer_buttons.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.button_save = wx.Button( self, wx.ID_ANY, u"Speichern", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.button_save.Bind(wx.EVT_BUTTON, self.on_save)
        sizer_buttons.Add( self.button_save, 0, wx.ALL, 5 )
        
        self.button_delete = wx.Button( self, wx.ID_ANY, u"Löschen", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.button_delete.Bind(wx.EVT_BUTTON, self.on_delete)
        sizer_buttons.Add( self.button_delete, 0, wx.ALL, 5 )
        
        self.button_cancel = wx.Button( self, wx.ID_ANY, u"Abbruch", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.button_cancel.Bind(wx.EVT_BUTTON, self.on_close)
        sizer_buttons.Add( self.button_cancel, 0, wx.ALL, 5 )
        
        sizer_main.Add( sizer_buttons, 1, wx.EXPAND, 5 )
        
        self.SetSizer( sizer_main )
        self.error_dialog = Dialogs.Error(self)
        
        self.Layout()
        self.Centre( wx.BOTH )
        self.Show()
        
        
    def on_close(self, event=None):
        self.Destroy()



class CustomFormDialog(wx.Dialog, DatabaseFormBase):
    def __init__(self, parent=None,
                       icon_path=None,
                       title='',
                       xrc_path=None,
                       panel_name=None,
                       remote_parent=None,
                       permissions={}):
        
        DatabaseFormBase.__init__(self, parent, icon_path, title, xrc_path, panel_name, remote_parent, permissions)
        wx.Dialog.__init__(self, self.parent, wx.ID_ANY, self.title, size=(800, 480), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        if icon_path <> None:
            self.SetIcon(wx.Icon(self.icon_path, wx.BITMAP_TYPE_ICO))
        
        sizer_main = wx.FlexGridSizer( 2, 1, 0, 0 )
        sizer_main.AddGrowableCol( 0 )
        sizer_main.AddGrowableRow( 0 )
        sizer_main.SetFlexibleDirection( wx.BOTH )
        sizer_main.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        sizer_main.Add( self.form, 1, wx.EXPAND |wx.ALL, 5 )
        
        sizer_buttons = wx.BoxSizer( wx.HORIZONTAL )
        sizer_buttons.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.button_save = wx.Button( self, wx.ID_ANY, u"Speichern", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.button_save.Bind(wx.EVT_BUTTON, self.on_save)
        sizer_buttons.Add( self.button_save, 0, wx.ALL, 5 )
        
        self.button_delete = wx.Button( self, wx.ID_ANY, u"Löschen", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.button_delete.Bind(wx.EVT_BUTTON, self.on_delete)
        sizer_buttons.Add( self.button_delete, 0, wx.ALL, 5 )
        
        self.button_cancel = wx.Button( self, wx.ID_ANY, u"Abbruch", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.button_cancel.Bind(wx.EVT_BUTTON, self.on_close)
        sizer_buttons.Add( self.button_cancel, 0, wx.ALL, 5 )
        
        sizer_main.Add( sizer_buttons, 1, wx.EXPAND, 5 )
        
        self.SetSizer( sizer_main )
        self.error_dialog = Dialogs.Error(self)
        
        self.Layout()
        self.Centre( wx.BOTH )
        
        
    def on_close(self, event=None):
        self.Destroy()



class SearchFrame(wx.Dialog):
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
        
        wx.Dialog.__init__(self, self.parent, wx.ID_ANY, self.title, size=(800, 480), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
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
        
        self.db_object = self.db_table.db_object
        
        self.error_dialog = Dialogs.Error(self)
        
        
#    def on_search(self, event=None):
#        widget_object = event.GetEventObject()
        
        
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
        
        self.entry_search = wx.SearchCtrl(parent=self.toolbar_standard, id=wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
        self.entry_search.SetDescriptiveText('Volltextsuche')
        
        self.toolbar_standard.AddControl(self.entry_search)

    
    def populate_table(self):
        self.table = DatabaseTableBase(self.db_table, portlet_parent=self.panel)
        self.table.edit = self.edit
        
        self.table.initialize(self.definition)
        self.table.create()
        
        
    def edit(self):
        self.add_dataset(self.table.Table.get_selected_row_content())
        self.remote_parent.populate()
        self.Close()
        
        
    def populate(self):
        pass
            
        

# Export -----------------------------------------------------------------------
class ExcelExport(wx.Dialog):
    def __init__(self):
        import pyExcelerator



# Print a table ----------------------------------------------------------------
class PrintTable():
    pass



# Print a form -----------------------------------------------------------------
class PrintForm():
    pass


