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
from config import *

from pprint import pprint


class DatabaseTableBase(object):
    def __init__(self, db_table, form=None, portlet_parent=None, editable=True, permissions={}):
        self.db_table = db_table
        self.db_object = db_table.db_object
        self.form = form
        self.portlet_parent = portlet_parent
        self.editable = editable
        
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
        
        
    # Actions -----------------------------------------------------------------
    def new(self, *args, **kwargs):
        if self.form == None:
            print 'no form defined!'
            return
        
        try:
            self.primary_key = None
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
                    add_text = str(inst[0])
                    self.ErrorDialog.show(title='Fehler', instance=inst, message=u'Fehler beim Löschen des Datensatzes!\n' + add_text)

                
    
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
        #TODO: Gay again, subclassing would help immensely!
        #self.Table = DataViews.Tree(self.portlet_parent)
        #print 'populating!'
        
        if content_lod == None:
            if self.filter == None and self.search_string == None:
                self.content_lod = self.db_table.get_content()
            elif self.filter == False:
                return
            else:
                clause = self.build_where_clause()
                self.content_lod = self.db_table.select(where=clause)
        else:
            self.content_lod = content_lod
            
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
        # TODO: Gaylord, would never ever be nesseccary if subclassed!
        self.Table.row_right_click_function = self.row_right_click_function
        
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
        
        
    def set_search_columns(self, search_columns):
        self.search_columns = search_columns
        

    def set_search_string(self, search_string):
        self.search_string = search_string #str(self.entry_search.GetValue())
        # print self.search_string, self.search_columns
        self.populate()
        

    def check_column_substitutions(self):
        ''' Search for one to one relationships in that table and if any there,
            call the do_column_substitutions function and replace them with content. ''' 
        
        for column_dic in self.definition_lod:
            if column_dic.has_key('populate_from'):
                populate_from = column_dic['populate_from']
                if column_dic.has_key('column_name'):
                    column_name = column_dic['column_name']
                    if column_dic.has_key('referenced_table_object'):
                        referenced_table_object = column_dic['referenced_table_object']
                        column_dic['referenced_column_name'] = column_dic.get('referenced_table_object').get_primary_key_columns()[0]
                        if column_dic.has_key('referenced_column_name'):
                            referenced_column_name = column_dic['referenced_column_name']                                        
                            mask = column_dic.get('mask')
                            self.do_column_substitutions(column_name, populate_from, mask, referenced_table_object, referenced_column_name)
        
        
    def do_column_substitutions(self, column_name, populate_from, mask, referenced_table_object, referenced_column_name):
        ''' Substitute foreign keys with content from the foreign tables. '''
        
        #TODO: This is bullshit, because it steals the foreign keys from the dict!
        # Make it work, so that the content of the content_lod will not be changed.
        # This is only possible, if the following code moved nearly entirely to the
        # populate function!
        # 
        # Another note on this:
        # it prevents from making multiple 'populate_from' definitions work, because
        # this replaces the foreign_key on its first execution and thus, a second call
        # on the same foreign_key_column is not possible.
        #
        # This should be solved like that:
        # in the database table definition should be defined, which columns from the foreign
        # table are used (like it does now). Then, this framework should create new columns
        # to show them!
        
        for content_dic in self.content_lod:
            substitute_dic = {}
            foreign_key = content_dic[column_name]
            if foreign_key in [None, 'NULL']:
                continue
            
            substitute_lod = referenced_table_object.select(column_list=populate_from, where='%s = %i' % (referenced_column_name, foreign_key))
            if mask == None:
                mask = u'%(' +'%s' % populate_from[0] + u')s'
            else:
                mask = u'%s' % mask
                
            if substitute_lod <> []:
                substitute_dict = substitute_lod[0]
                for key in substitute_dict:
                    content = str(substitute_dict[key]) 
                    substitute_dict[key] = '%s' % str(content)            
                
                content_dic[column_name] = str(mask) % substitute_dict

            
    
class SubTable(DatabaseTableBase):
    def __init__(self, db_table, form=None, portlet_parent=None, parent_form=None, editable=True, permissions={}):
        DatabaseTableBase.__init__(self, db_table, form, portlet_parent, editable, permissions)
        
        self.editable = editable
        self.parent_form = parent_form
        self.permissions = permissions
        
        #print 'subtable_perms:', self.permissions
        self.sizer = wx.FlexGridSizer(1, 4, 0, 0)
        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableRow(0)
        self.sizer.SetFlexibleDirection( wx.BOTH )
        self.sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.portlet_parent.SetSizer(self.sizer)

        
    def on_add_clicked(self, event=None):
        self.new()
        #print 'add'
    
    
    def on_edit_clicked(self, event=None):
        self.edit()
        #print 'edit'
    
    
    def on_delete_clicked(self, event=None):
        self.delete()
        #print 'delete'
        
        
    def populate_portlet(self):
        super(SubTable, self).populate_portlet()
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
    ID_NEW = 101
    ID_EDIT = 102
    ID_DELETE = 103
    
    ID_PRINT = 201
    ID_EXPORT_TABLE = 202
    #ID_PREFERENCES = 401
    ID_HELP = 402
    
    
    def __init__(self, db_table, form=None, \
                 toolbar_parent=None, portlet_parent=None, \
                 help_path=None, permissions={}):
        
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
        
    
    def on_search(self, event=None):
        self.set_search_string(self.entry_search.GetValue())
        
        
    def on_export(self, event=None):
        print "export"
        
        
    def on_preferences(self, event=None):
        #self.frame_preferences = FormTablePreferences(parent=toplevel_frame, title='Einstellungen', remote_parent=self)
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
        
        if self.permissions.get('print') <> False:
            self.toolbar_parent.AddTool(self.ID_PRINT, "Drucken",          IconSet16.getprint_16Bitmap(), 'drucken')
            self.toolbar_parent.Bind(wx.EVT_TOOL, self.on_print, id=self.ID_PRINT)
        
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
        combobox_filter = wx.ComboBox(
            parent=self.toolbar_parent, id=-1, choices=['<alle>'],
            size=(150,-1), style=wx.CB_DROPDOWN)
        combobox_filter.SetToolTip(wx.ToolTip('Filter'))
        self.toolbar_parent.AddControl(combobox_filter)
        
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
        #wx.Frame.__init__(self, self.parent, wx.ID_ANY, self.title, size=(800, 480))
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
        self.table.populate_portlet()
        
        
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
                       remote_parent=None,
                       permissions={}):
        
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
        self.permissions = permissions
        
        #print 'form:', self.permissions
        
        # This lists are made to get portlets going.
        self.save_function_list = []
        self.delete_function_list = []
        self.print_function_list = []
        
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
                add_text = str(inst[0])
                self.error_dialog.show(instance=inst, message='Beim löschen dieses Datensatzes ist ein Fehler aufgetreten!\n' + add_text)
        
        
    def on_print(self, event=None):
        #TODO: It would be better if self would be given on_delete and on_save.
        for function in self.print_function_list:
            function(self)
            
        
    def on_preferences(self, event=None):
        self.frame_preferences = FormTablePreferences(parent=self, title='Einstellungen', remote_parent=self)
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
            referenced_table_object = dic.get('referenced_table_object')
            referenced_column_name = dic.get('referenced_column_name')
            widget_object = dic.get('widget_object')
            column_name = dic.get('column_name')
            fill_distinct = dic.get('fill_distinct')
            on_populate = dic.get('on_populate')
            
            enable_list = self.permissions.get('enable')
            if type(enable_list) == list:
                if column_name not in enable_list:
                    widget_object.Enable(False)
                    
            if fill_distinct == True:
                result = self.db_table.select(distinct=True, column_list=[column_name], listresult=True)
                for item in result:
                    if item == None:
                        continue
                    widget_object.Append(item)
                
            if on_populate <> None:
                on_populate(dic)
                
            if populate_from == None:
                continue
            if mask == None:
                mask = '%(' +'%s' % populate_from[0] + ')s'
                
            populate_from.append(referenced_column_name)
            #referenced_table_object = SQLdb.table(self.db_object, referenced_table_name)
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
        
        
    def get_widget(self, widget_name):
        widget = self.form.get_widget(widget_name)
        return widget
    
    
    def add_save_function(self, function):
        self.save_function_list.append(function)
        
    
    def add_delete_function(self, function):
        self.delete_function_list.append(function)
        
        
    def add_print_function(self, function):
        self.print_function_list.append(function)
        
        
        