# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wxPortlets module.
# by Mark Muzenhardt, published under LGPL license.
#===============================================================================

import wx, wx.aui

from misc import FileSystem, HelpFile, FileTransfer
from wxApi import Panels, Dialogs, DataViews, Toolbars
from wxApi import Transformations as WxTransformations
from wxApi.res import IconSet16
from dbApi import SQLdb, Tools as dbTools

from pprint import pprint


class WebserverPreferences:
    pass
    
    
class FormTable:
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
        
        self.db_table = db_table
        self.toolbar_parent = toolbar_parent
        self.portlet_parent = portlet_parent
        self.form = form
        self.help_path = help_path
        
        # TODO: remove this sheenanigan asap!
        self.parent_form = None
        
        self.ErrorDialog = Dialogs.Error(parent=self.portlet_parent)
        self.HelpDialog = Dialogs.Help(parent=self.portlet_parent)
        
    
    # Callbacks ---------------------------------------------------------------
    def on_row_activate(self, content_dic=None):
        self.primary_key = content_dic[self.primary_key_column]
        self.on_edit()


    def on_cursor_changed(self, content_dic=None):
        self.toolbar_parent.EnableTool(self.ID_EDIT, True)
        self.toolbar_parent.EnableTool(self.ID_DELETE, True)
        
        self.primary_key = content_dic[self.primary_key_column]
        # print self.primary_key
        

    # Actions -----------------------------------------------------------------
    def on_new(self, event=None):
        if self.form == None:
            return
        
        try:
            self.primary_key = None
            self.form(parent=self.portlet_parent, remote_parent=self)
        except Exception, inst:
            self.ErrorDialog.show('Fehler', inst, message='Beim öffnen des Formulars ist ein Fehler aufgetreten!')
            
            
    def on_edit(self, event=None):
        if self.form == None:
            return

        form_instance = self.form(parent=self.portlet_parent, remote_parent=self)
        form_instance.populate()


    def on_delete(self, event=None):
        if self.primary_key <> None:
            dialog = wx.MessageDialog(None, u'Soll dieser Datensatz wirklich gelöscht werden?', 'Frage', 
                                    wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            answer = dialog.ShowModal()
            if answer == wx.ID_YES:
                pk_column = self.db_table.get_primary_key_columns()[0]
                self.db_table.delete(where='%s = %s' % (pk_column, self.primary_key))
                self.populate()


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
        if self.parent_form <> None: 
            if self.parent_form.primary_key <> None:
                # This populates a referenced table (on a parent form)
                attributes_lod = self.db_table.attributes
                primary_key_column = self.primary_key_column
                referenced_table_name = self.parent_form.db_table.name
                
                self.foreign_key_column_name = \
                    self.db_table.get_foreign_key_column_name(attributes_lod, 
                                                              primary_key_column, 
                                                              referenced_table_name)
                
                self.content_lod = self.db_table.select(where='%s = %i' % (self.foreign_key_column_name, self.parent_form.primary_key))
            else:
                # This clears the table if parent form has no primary_key (f.e. if a new dataset is created!
                self.content_lod = []
        else:
            self.content_lod = self.db_table.get_content()

        # Before populating, check if there are any substitutions from referenced tables
        self.check_column_substitutions()
        self.Table.populate(self.content_lod)
        
        # Do callbacks for the population of higher-level widgets.
        for definition_dic in self.definition_lod:
            if definition_dic.has_key('populate_function'):
                definition_dic['populate_function'](definition_dic)
                
                
    def update(self):
        self.button_new.set_sensitive(1)
        self.button_delete.set_sensitive(0)
        self.button_edit.set_sensitive(0)
        
        self.populate()


    def populate_toolbar(self):
        self.toolbar_parent.SetToolBitmapSize(wx.Size(22, 22))
        
        if self.form <> None:
            self.toolbar_parent.AddTool(self.ID_NEW,  "Neu",        IconSet16.getfilenew_16Bitmap())
            self.toolbar_parent.Bind(wx.EVT_TOOL, self.on_new, id=self.ID_NEW)
    
            self.toolbar_parent.AddTool(self.ID_EDIT,  "Bearbeiten", IconSet16.getedit_16Bitmap())
            self.toolbar_parent.Bind(wx.EVT_TOOL, self.on_edit, id=self.ID_EDIT)
    
            self.toolbar_parent.AddTool(self.ID_DELETE, u"Löschen",    IconSet16.getdelete_16Bitmap())
            self.toolbar_parent.Bind(wx.EVT_TOOL, self.on_delete, id=self.ID_DELETE)
    
            self.toolbar_parent.AddSeparator()
        
        self.toolbar_parent.AddTool(self.ID_PRINT, "Drucken",     IconSet16.getprint_16Bitmap())
        self.toolbar_parent.Bind(wx.EVT_TOOL, self.on_print, id=self.ID_PRINT)

        #if filter == True:
        self.toolbar_parent.AddSeparator()
        combobox_filter = wx.ComboBox(
            parent=self.toolbar_parent, id=-1, choices=["", "This", "is a", "wx.ComboBox"],
            size=(150,-1), style=wx.CB_DROPDOWN)
        self.toolbar_parent.AddControl(combobox_filter)
        
        #if search == True:
        self.toolbar_parent.AddSeparator() 
        entry_search = wx.SearchCtrl(parent=self.toolbar_parent, id=-1)
        self.toolbar_parent.AddControl(entry_search) 
        
        #if preferences == True or help == True:
        self.toolbar_parent.AddSeparator()
        
        # These lines have to be in the Preferences-Dialog!
        #self.toolbar_parent.AddTool(self.ID_IMPORT, "Importieren", IconSet16.getfileimport_16Bitmap())
        #self.toolbar_parent.Bind(wx.EVT_TOOL, self.on_import, id=self.ID_IMPORT)
        
        #self.toolbar_parent.AddTool(self.ID_EXPORT, "Exportieren", IconSet16.getfileexport_16Bitmap())
        #self.toolbar_parent.Bind(wx.EVT_TOOL, self.on_export, id=self.ID_EXPORT)
        
        #if preferences == True:
        self.toolbar_parent.AddTool(self.ID_PREFERENCES, "Einstellungen", IconSet16.getpreferences_16Bitmap())
        self.toolbar_parent.Bind(wx.EVT_TOOL, self.on_preferences, id=self.ID_PREFERENCES)
        
        if self.help_path <> None:
            self.toolbar_parent.AddLabelTool(self.ID_HELP, label="Hilfe",         bitmap=IconSet16.gethelp_16Bitmap())
            self.toolbar_parent.Bind(wx.EVT_TOOL, self.on_help, id=self.ID_HELP)
        
        self.toolbar_parent.Realize()
    
    
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
        #print 'set filter to:', filter_name
        
        
    def check_column_substitutions(self):
        for column_dic in self.definition_lod:
            if column_dic.has_key('populate_from'):
                populate_from = column_dic['populate_from']
                if column_dic.has_key('column_name'):
                    column_name = column_dic['column_name']
                    if column_dic.has_key('referenced_table_name'):
                        referenced_table_name = column_dic['referenced_table_name']
                        if column_dic.has_key('referenced_column_name'):
                            referenced_column_name = column_dic['referenced_column_name']                                        
                            if column_dic.has_key('mask'):
                                mask = column_dic['mask']
                                self.do_column_substitutions(column_name, populate_from, mask, referenced_table_name, referenced_column_name)
        
        
    def do_column_substitutions(self, column_name, populate_from, mask, referenced_table_name, referenced_column_name):
        for content_dic in self.content_lod:
            substitute_dic = {}
            foreign_key = content_dic[column_name]
            if foreign_key in [None, 'NULL']:
                return
            substitute_lod = self.db_object.select(table_name=referenced_table_name, column_list=populate_from, where='%s = %i' % (referenced_column_name, foreign_key))
            content_dic[column_name] = mask % substitute_lod[0]
        
    
    
class FormFrame(wx.Frame):
    ID_SAVE = 101
    ID_DELETE = 102
    ID_PRINT = 103
    
    ID_PREFERENCES = 201
    ID_HELP = 202
    
    def __init__(self, remote_parent=None,
                       parent=None,
                       title='',
                       panel_name=None,
                       icon_path=None,
                       xrc_path=None,
                       help_path=None):
        
        ''' db_table is the the table in which this Form writes the data. The remote_parent
            is triggered on save and close, so that the parent widget can be updated. parent
            is simply the wxWidgets-Parent, usually a Frame. title is the Frame-title, 
            panel_name is the name of the panel which is loaded from the file behind xrc_path.
            The help-path enables online help, if given. '''
            
        self.remote_parent = remote_parent
        self.parent = parent 
        self.title = title
        self.panel_name = panel_name
        self.icon_path = icon_path
        self.xrc_path = xrc_path
        self.help_path = help_path
        
        wx.Frame.__init__(self, self.parent, wx.ID_ANY, self.title)
        self.SetIcon(wx.Icon(self.icon_path, wx.BITMAP_TYPE_ICO))
        self.Bind(wx.EVT_CLOSE, self.on_close)
        
        self.aui_manager = wx.aui.AuiManager(self)
        
        self.panel_main = wx.Panel(self, -1, size = (320, 240))
        self.create_toolbar()
        
        self.aui_manager.AddPane(self.toolbar_standard, wx.aui.AuiPaneInfo().
                         Name("toolbar_standard").Caption("Standard").
                         ToolbarPane().Top().Resizable().
                         LeftDockable(False).RightDockable(False))
        self.aui_manager.AddPane(self.panel_main, wx.aui.AuiPaneInfo().CaptionVisible(False).
                                 Name("panel_main").TopDockable(False).
                                 Center().Layer(1).CloseButton(False))
        self.aui_manager.Update()
        self.Show()
        
        self.db_table = remote_parent.db_table
        self.primary_key = None
        if self.remote_parent.primary_key <> None:
            self.primary_key = self.remote_parent.primary_key
        
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
                print 'writing:'
                print form_content
                print 'primary key: ', self.primary_key
                self.db_table.update(form_content, where='%s = %s' % (pk_column, self.primary_key))
            else:
                self.db_table.insert(key_column=pk_column, content=form_content)
        except Exception, inst:
            self.error_dialog.show(instance=inst, message='Beim speichern dieses Datensatzes ist ein Fehler aufgetreten!')
        
        self.remote_parent.populate()
        self.on_close()
        
        
    def on_delete(self, event=None):
        print 'delete formular'
        
        
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
        
        self.form = DataViews.Form(self.panel_main, self.xrc_path, self.panel_name)
        self.form.initialize(definition_lod=self.definition_lod, 
                             attributes_lod=self.attributes_lod)
        self.definition_lod = self.form.definition_lod
        self.SetInitialSize()
        
        
    def populate(self):
        if self.primary_key <> None:
            pk_column = self.db_table.get_primary_key_columns()[0]
            content_lod = self.db_table.select(where='%s = %s' % (pk_column, self.primary_key))
            self.form.populate(content_dict=content_lod[0])
        # else:
        #    content_lod = None
    
    
    def create_toolbar(self, dataset=True, report=True, help=True):
        self.toolbar_standard = wx.aui.AuiToolBar(self, id=wx.ID_ANY) 
        
        self.toolbar_standard.AddTool(self.ID_SAVE, "Speichern", IconSet16.getfilesave_16Bitmap())
        self.toolbar_standard.Bind(wx.EVT_TOOL, self.on_save, id=self.ID_SAVE)
        
        self.toolbar_standard.AddTool(self.ID_DELETE, "Löschen", IconSet16.getdelete_16Bitmap())
        self.toolbar_standard.Bind(wx.EVT_TOOL, self.on_delete, id=self.ID_DELETE)
        
        self.toolbar_standard.AddTool(self.ID_PRINT, "Drucken", IconSet16.getprint_16Bitmap())
        self.toolbar_standard.Bind(wx.EVT_TOOL, self.on_print, id=self.ID_PRINT)
        
        self.toolbar_standard.AddSeparator()
        self.toolbar_standard.AddTool(self.ID_PREFERENCES, "Einstellungen", IconSet16.getpreferences_16Bitmap())
        self.toolbar_standard.Bind(wx.EVT_TOOL, self.on_preferences, id=self.ID_PREFERENCES)
        
        self.toolbar_standard.AddTool(self.ID_HELP, "Hilfe", IconSet16.gethelp_16Bitmap())
        self.toolbar_standard.Bind(wx.EVT_TOOL, self.on_help, id=self.ID_HELP)
        
        
        
class OldForm(wx.Frame):
    def __init__(self, parent=None,
                       parent_form=None, 
                       title=None, 
                       panel_name=None,
                       icon_path=None, 
                       xrc_path=None,     
                       help_path=None):
        self.parent = parent
        self.parent_form = parent_form
        self.primary_key_column = None
        self.primary_key = None
        
        self.frame = None
        self.icon_path = icon_path
        self.title = title
        self.xrc_path = xrc_path
        self.panel_name = panel_name
        self.help_path = help_path
        print 'init Form instance'
        
        wx.Frame.__init__(self, self.parent, wx.ID_ANY, self.title)
        
        self.Show()
        
        self.aui_manager = wx.aui.AuiManager(self)
        
        self.create_toolbar()

        # Add panels ----------------------------------------------------------
        self.panel_main = wx.Panel(self, -1, size = (200, 150))

        self.aui_manager.AddPane(self.toolbar_standard, wx.aui.AuiPaneInfo().
                         Name("toolbar_standard").Caption("Standard").
                         ToolbarPane().Top().Resizable().
                         LeftDockable(False).RightDockable(False))
        self.aui_manager.AddPane(self.panel_main, wx.aui.AuiPaneInfo().CaptionVisible(True).
                                 Name("panel_main").TopDockable(False).
                                 Center().Layer(1).CloseButton(False))
        self.aui_manager.Update()
        self.SetInitialSize()
        
        
    #def on_button_save_clicked(self, widget=None, data=None):
    #    self.save_dataset()
    #    self.window.destroy()


    #def on_button_delete_clicked(self, widget=None, data=None):
    #    self.delete_dataset()

    
    #def on_button_print_clicked(self, widget=None, data=None):
    #    pass


    #def on_button_help_clicked(self, widget=None, data=None):
    #    if self.help_path <> None:
    #        self.HTMLhelp.show(self.help_path)


    #def on_window_destroy(self, widget=None, data=None):
    #    if self.portlets_lod <> None:
    #        for portlet_row in self.portlets_lod:
    #            dic = portlet_row
    #            if dic.has_key('portlet'):
    #                if dic.has_key('container'):
    #                    self.xrc.get_widget(dic['container']).remove(dic['portlet'])
    #    self.update_func()


    # Actions -----------------------------------------------------------------
    def show(self, primary_key=None):
        ''' This is for all stuff on the Form which is not standard.
            portlets_lod = [{'portlet': None,
                                 => widget_object to be drawn to the container
                             'container': None,
                                 => container to draw the widget in
                             'save_function': None,
                                 => function triggered on save
                             'update_function': None,
                                 => function triggered if form is shown
                             'delete_function': None}]
                                 => function triggered on delete'''
        
        #self.frame = wx.Frame(self.parent, wx.ID_ANY, self.title)
        
        
        self.primary_key = primary_key

        if self.help_path <> None:
            help_button_visible = True

        
        
        #self.pane_main_info = self.aui_manager.GetPane('self.panel_main')
                
        
        # Get wTree, initialize form
        self.Form = DataViews.Form(self.panel_main, self.xrc_path, self.panel_name)
        self.Form.initialize(definition_lod=self.definition_lod, 
                             attributes_lod=self.attributes_lod)
        self.definition_lod = self.Form.definition_lod

        # Get the portlet_objects and pack them into their container.
        #if self.portlets_lod <> None:
        #    for portlet_row in self.portlets_lod:
        #        dic = portlet_row
        #        if dic.has_key('portlet'):
        #            if dic.has_key('container'):
        #                container = self.wTree.get_widget(dic['container'])
        #                container.add(dic['portlet'])
        #                if dic.has_key('populate_function'):# and self.primary_key <> None:
        #                    dic['populate_function']()
        
        
        

    def create_toolbar(self, dataset=True, report=True, help=True):
        self.toolbar_standard = wx.aui.AuiToolBar(self, id=wx.ID_ANY) 
 
        self.toolbar_standard.AddTool(wx.ID_ANY, "Speichern",     IconSet16.getfilesave_16Bitmap())
        self.toolbar_standard.AddTool(wx.ID_ANY, "Löschen",       IconSet16.getdelete_16Bitmap())
        self.toolbar_standard.AddTool(wx.ID_ANY, "Drucken",       IconSet16.getprint_16Bitmap())
        self.toolbar_standard.AddSeparator()
        self.toolbar_standard.AddTool(wx.ID_ANY, "Einstellungen", IconSet16.getpreferences_16Bitmap())
        self.toolbar_standard.AddTool(wx.ID_ANY, "Hilfe",         IconSet16.gethelp_16Bitmap())


    def initialize(self, db_table=None, definition_lod=None, attributes_lod=None, portlets_lod=None):
        ''' This initializes the Form. Following Data exchanges are to met:

            definition_lod = [{'column_name': 'id',
                                   => column which holds the content of this widget.
                               'widget_name': 'entry_name',
                                   => glade name of widget
                               'widget_object': gtk.Entry,
                                   => real object of the widget, filled automatically by glade!
                               'validation_function': self.validate,
                                   => if the attributes_lod can not validate automatically, use this.
                               'population_function': self.populate,
                                   => for combobox(entrys), tables and other nasty to-populate-mess!
                               'editable': True}]

            attributes_lod = [{'column_name': 'id'

                               'data_type': 'bigint'
                               'character_maximum_length': = 20
                               'numeric_precision' = 2
                               'numeric_scale' = ?
                               'is_nullable' = True}] 
                               
            portlets_lod = [{'portlet':   portlet_object,
                             'container': 'alignment_address' '''

        self.db_table = db_table
        
        self.definition_lod = definition_lod
        self.attributes_lod = attributes_lod
        self.portlets_lod = portlets_lod
        
        result = WxTransformations.search_lod(self.attributes_lod, 'is_primary_key', True)
        if result <> None: 
            self.primary_key_column = result['column_name']
                        
                        
    def populate(self):
        if self.primary_key <> None:
            content_lod = self.db_table.db_object.dictresult('''\
SELECT * FROM %s WHERE %s = %s''' % (self.db_table.name, 
                                     self.primary_key_column, 
                                     self.primary_key))
            self.Form.populate(content_dict=content_lod[0])
        else:
            content_lod = None
        
        # Do callbacks for the population of higher-level widgets.
        for definition_dic in self.definition_lod:
            # First, check if there is a referenced table. If content_lod is empty,
            # pass through to populate the comboboxentry-dropdown-tables!
            foreign_content_dic = None
            if definition_dic.has_key('referenced_table_name'):
                if content_lod <> None:
                    foreign_key = content_lod[0][definition_dic['column_name']]
                else:
                    foreign_key = None
                    
                if foreign_key == None:
                    foreign_key = 'NULL'
                
                foreign_content_lod = self.db_table.db_object.dictresult('''\
SELECT * FROM %s WHERE %s = %s''' % (definition_dic['referenced_table_name'], 
                             definition_dic['referenced_column_name'], 
                             foreign_key))
                if foreign_content_lod <> []:
                    foreign_content_dic = foreign_content_lod[0]
            
            # Second, check if there is a populate function
            if definition_dic.has_key('populate_function'):
                definition_dic['populate_function'](definition_dic['widget_object'], foreign_content_dic)
            
            # Perhaps there is a simple populate_from attribute?
            if definition_dic.has_key('populate_from'):
                populate_from = definition_dic['populate_from']
                if definition_dic.has_key('referenced_table_name'):
                    referenced_table_name = definition_dic['referenced_table_name']
                    referenced_column_name = definition_dic['referenced_column_name']
                    widget = definition_dic['widget_object']
                    
                    if definition_dic.has_key('mask'):
                        mask = definition_dic['mask']
                    else:
                        mask = None
                    
                    populate_from.append(referenced_column_name) 
                    foreign_table = SQLdb.table(self.db_object, referenced_table_name)
                    result_lod = foreign_table.select(populate_from)
                    widget.initialize({'column_name': [populate_from][0], 'mask': mask})
                    widget.populate(result_lod)
                    
                    if foreign_content_dic <> None:
                        widget.set_text(foreign_content_dic[populate_from[0]])
                            

    def save_dataset(self):
        try:
            form_content_dict = self.Form.get_content()
            
            # First, save the parent form!
            if self.parent_form <> None:
                self.parent_form.save_dataset()
                
                # This saves data to the referenced column.
                attributes_lod = self.db_table.attributes
                primary_key_column = self.primary_key_column
                referenced_table_name = self.parent_form.db_table.name
                
                self.foreign_key_column = \
                    self.db_table.get_foreign_key_column_name(attributes_lod, 
                                                              primary_key_column, 
                                                              referenced_table_name)
                
                form_content_dict[self.foreign_key_column] = self.parent_form.primary_key
                
            if self.primary_key == None:
                self.primary_key = self.db_table.get_last_primary_key('id') + 1
                form_content_dict[self.primary_key_column] = self.primary_key
                self.db_table.insert(primary_key_column=self.primary_key_column, content=form_content_dict)
            else:
                form_content_dict[self.primary_key_column] = self.primary_key
                self.db_table.update(primary_key_column=self.primary_key_column, content_dict=form_content_dict)
            
            # At last, do all the save functions of the portlets that have any.
            if self.portlets_lod <> None:
                for portlet_dic in self.portlets_lod:
                    if portlet_dic.has_key('save_function'):
                        portlet_dic['save_function'](self.primary_key)
        except Exception, inst:
            self.DialogBox.show(dialog_type='error', title='Fehler', inst=inst)


    def delete_dataset(self):
        if self.primary_key <> None:
            response = self.DialogBox.show(dialog_type='yesno', title='Frage', text='Soll dieser Datensatz wirklich gelöscht werden?')
            if response == 'YES':
                try:
                    if self.portlets_lod <> None:
                        for portlet_dic in self.portlets_lod:
                            if portlet_dic.has_key('delete_function'):
                                portlet_dic['delete_function'](self.primary_key)
                            
                    self.db_table.delete(self.primary_key_column, self.primary_key)
                except Exception, inst:
                    self.DialogBox.show(dialog_type='error', inst=inst)
                    return False
                self.window.destroy()
                return True
            else:
                return False
            

    def set_update_function(self, update_func):
        ''' This sets the function triggered with saving and closing. '''

        self.update_func = update_func
        