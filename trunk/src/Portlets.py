# -*- coding: iso-8859-1 -*-

#===============================================================================
# Portlets module.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import sys
import gtk

from Commons import FileSystem, HelpFile
from GTK import Containers, Dialogs, DataViews, Buttons, Glade, Portlets
from GTK import Transformations as GTK_Transformations
from DB  import SQLdb

from pprint import pprint

#print 'GTK_Transformations:', GTK_Transformations


class DatabaseLogin:
    ''' Multifunctional portlet which reads a database configuration
        from an ini-File and connects it. '''

    def __init__(self, ini_filename='', autosave=False, parent=None):
        self.ini_filename = ini_filename
        self.autosave = autosave
        self.parent = parent
        self.database = None

        self.database_dialog = Dialogs.Database()
        self.DialogBox = Dialogs.Simple(parent=self.parent)
        self.ini_file = FileSystem.iniFile(self.ini_filename)
        self.portlet = self.database_dialog.create()
        
        db_engines_list = SQLdb.get_engines()
        self.config_dic = self.get_settings_from_ini()
        
        if sys.platform.startswith('win'):
            odbc_drivers_list = self.get_odbc_from_winreg()
        else:
            odbc_drivers_list = []
            
        self.database_dialog.populate(db_engines_list, odbc_drivers_list, self.config_dic)

        self.database_dialog.connect_order = self.connect_db
        self.database_dialog.disconnect_order = self.disconnect_db


    # Foreign actions ---------------------------------------------------------
    def set_connect_function(self, on_connect):
        self.database_dialog.on_connect = on_connect


    def set_disconnect_function(self, on_disconnect):
        self.database_dialog.on_disconnect = on_disconnect


    def get_settings_from_db(self, database):
        self.database = database
        if self.database <> None:
            self.config_dic = database.config
        else:
            self.database_dialog.set_disconnected()
            return

        if self.database.connection <> None:
            self.database_dialog.set_connected()
        else:
            self.database_dialog.set_disconnected()
        return self.config_dic


    def get_settings_from_ini(self):
        try:
            self.config_dic = self.ini_file.dictresult('db')
            return self.config_dic
        except Exception, inst:
            error_text = """\
Während des Einlesens der Datenbank-Konfiguration ist folgender Fehler aufgetreten:

<b>%s</b>

Soll die Konfigurationsdatei neu erstellt werden?""" % str(inst)
            answer = self.DialogBox.show(dialog_type='yesno', title='Frage', text=error_text)
            if answer == 'YES':
                self.config_dic = self.save_settings_to_ini()
                return self.config_dic


    def get_odbc_from_winreg(self):
        import _winreg
        key =  _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\ODBC\\ODBCINST.INI")
        info = _winreg.QueryInfoKey(key)
        
        drivers_list = []
        number_of_keys = info[0]
        for number in xrange(number_of_keys):
            drivers_list.append(_winreg.EnumKey(key, number))
        return drivers_list
        
        
    def save_settings_to_ini(self):
        self.config_dic = self.database_dialog.get_config_dic()
        ini_text = """\
[db]
engine = %(engine)s
driver = %(driver)s
database = %(database)s
host = %(host)s
user = %(user)s
password = %(password)s

""" % self.config_dic

        self.ini_file.save(ini_text)
        return self.config_dic


    def connect_db(self):
        try:
            self.config_dic = self.database_dialog.get_config_dic()
            self.database = SQLdb.database(self.config_dic['engine'])
            self.database.connect(database=self.config_dic['database'],
                                  driver=self.config_dic['driver'],
                                  host=self.config_dic['host'],
                                  user=self.config_dic['user'],
                                  password=self.config_dic['password'])
            self.database_dialog.set_connected()
            
            # Save .ini-file automatically on connection
            if self.autosave == True:
                self.save_settings_to_ini()
        except Exception, inst:
            self.DialogBox.show(dialog_type='error', title='Fehler', inst=inst)
            self.database_dialog.set_disconnected()
        return self.database


    def disconnect_db(self):
        if self.database.connection <> None:
            self.database.close()
        self.database_dialog.set_disconnected()



class UserLogin:
    def __init__(self, content_lod=[], merge_field_list=[], parent=None):
        ''' content_lod = [{'id': 5, 'user': 'Frank, 'password': 'foobar'}] '''
 
        self.merge_field_list = merge_field_list
        self.content_lod = GTK_Transformations.merge_lod_fields(content_lod, 
                                                                self.merge_field_list, 
                                                                '#merged_fields')
        self.parent = parent

        self.login_dialog = Dialogs.Login()
        self.portlet = self.login_dialog.create()

        self.comboboxentry_user = self.login_dialog.comboboxentry_user
        self.comboboxentry_user.initialize(definition_dic = {'column_name': '#merged_fields'})
        
        self.comboboxentry_user.populate(self.content_lod)
        self.person = None
        
        #import hashlib
        #print hashlib.sha224("Nobody inspects the spammish repetition").hexdigest()


    def update_person_selection(self):
        self.person = self.comboboxentry_user.get_selection()


    def populate_persons(self, content_lod):
        #result = person_table_object.select([id_column, firstname_column, lastname_column])
        #names_lod = []
        #for dic in result:
        #    tmp_dic = {'fullname': '%s, %s' % (dic[lastname_column], dic[firstname_column]), 'id': dic[id_column]}
        #    names_lod.append()
        return #persons


    #def get_password(self, sql_command):
    #    return #password



class Table:
    def __init__(self, form_object=None, parent_form=None, dataset=True, report=False, search=False, filter=True, help=True, db_table=None, help_file=None, separate_toolbar=True):
        self.parent_form = parent_form
        
        self.help_file = help_file
        self.filter_lod = []
        
        self.Table = DataViews.Tree()
        self.Table.create()
        self.Table.set_row_activate_function(self.on_row_activate)
        self.Table.set_cursor_changed_function(self.on_cursor_changed)

        self.create_toolbar(dataset, report, search, filter, help)
        self.form = form_object
        self.form.set_update_function(self.update)
        
        self.scrolledwindow = gtk.ScrolledWindow()
        self.scrolledwindow.set_policy(hscrollbar_policy=gtk.POLICY_AUTOMATIC, 
                                       vscrollbar_policy=gtk.POLICY_AUTOMATIC)
        self.scrolledwindow.add(self.Table.widget)
        self.portlet = self.scrolledwindow

        if separate_toolbar == False:
            vbox = gtk.VBox()
            vbox.pack_start(child=self.toolbar,        expand=False, fill=True, padding=0)
            vbox.pack_start(child=self.scrolledwindow, expand=True,  fill=True, padding=0)
            self.portlet = vbox
        self.portlet.show()
        
        self.DialogBox = Dialogs.Simple(parent=None)
        self.HTMLhelp = HelpFile.HTML()
        

    # Callbacks ---------------------------------------------------------------
    def on_button_new_clicked(self, widget=None, data=None):
        self.new_dataset()


    def on_button_edit_clicked(self, widget=None, data=None):
        self.edit_dataset()


    def on_button_delete_clicked(self, widget=None, data=None):
        self.delete_dataset()


    def on_button_print_clicked(self, widget=None, data=None):
        self.print_dataset()


    def on_button_search_clicked(self, widget=None, data=None):
        self.search_dataset()


    def on_button_help_clicked(self, widget=None, data=None):
        self.show_help()


    def on_row_activate(self, content_dic=None):
        self.primary_key = content_dic[self.primary_key_column]
        self.edit_dataset()


    def on_cursor_changed(self, content_dic=None):
        self.button_edit.set_sensitive(1)
        self.button_delete.set_sensitive(1)
        self.primary_key = content_dic[self.primary_key_column]
        

    # Actions -----------------------------------------------------------------
    def new_dataset(self):
        self.button_new.set_sensitive(0)
        self.button_edit.set_sensitive(0)
        self.form.show(primary_key=None)


    def edit_dataset(self):
        self.form.show(self.primary_key)


    def delete_dataset(self):
        response = self.DialogBox.show(dialog_type='yesno', title='Frage', text='Soll dieser Datensatz wirklich gelöscht werden?')
        if response == 'YES':
            try:
                self.db_table.delete(self.primary_key_column, self.primary_key)
            except Exception, inst:
                self.DialogBox.show(dialog_type='error', inst=inst)

            self.button_delete.set_sensitive(0)
            self.button_edit.set_sensitive(0)
            self.update()


    def print_dataset(self):
        print "print"


    def search_dataset(self):
        print "search"


    def show_help(self):
        if self.help_file <> None:
            self.HTMLhelp.show(self.help_file)


    def create_toolbar(self, dataset, report, search, filter, help):
        self.toolbar = gtk.Toolbar()

        # Dataset widgets
        if dataset == True:
            self.button_new = Buttons.Simple().create(stock_image=gtk.STOCK_NEW, height=32)
            self.button_new.connect('clicked', self.on_button_new_clicked)
            self.toolbar.add(self.button_new)
            self.button_edit = Buttons.Simple().create(stock_image=gtk.STOCK_EDIT, height=32)
            self.button_edit.connect('clicked', self.on_button_edit_clicked)
            self.button_edit.set_sensitive(0)
            self.toolbar.add(self.button_edit)
            self.button_delete = Buttons.Simple().create(stock_image=gtk.STOCK_DELETE, height=32)
            self.button_delete.connect('clicked', self.on_button_delete_clicked)
            self.button_delete.set_sensitive(0)
            self.toolbar.add(self.button_delete)
            separator = gtk.VSeparator()
            separator.set_size_request(8, 32)
            self.toolbar.add(separator)

        # Report widgets
        if report == True:
            self.button_print = Buttons.Simple().create(stock_image=gtk.STOCK_PRINT, height=32)
            self.button_print.connect('clicked', self.on_button_print_clicked)
            self.toolbar.add(self.button_print)
            separator = gtk.VSeparator()
            separator.set_size_request(8, 32)
            self.toolbar.add(separator)

        # Search widgets
        if search == True:
            self.entry_search = gtk.Entry()
            self.entry_search.set_size_request(200, 24)
            self.toolbar.add(self.entry_search)
            self.button_search = Buttons.Simple().create(stock_image=gtk.STOCK_FIND, height=32)
            self.button_search.connect('clicked', self.on_button_search_clicked)
            self.toolbar.add(self.button_search)
            separator = gtk.VSeparator()
            separator.set_size_request(8, 32)
            self.toolbar.add(separator)

        # Filter widgets
        if filter == True:
            self.comboboxentry_filter = gtk.ComboBoxEntry()
            self.comboboxentry_filter.set_size_request(200, 24)
            vbox = gtk.VBox()
            vbox.pack_start(gtk.Fixed(), expand=True, fill=True, padding=0)
            vbox.pack_start(self.comboboxentry_filter, expand=False, fill=False, padding=0)
            vbox.pack_start(gtk.Fixed(), expand=True, fill=True, padding=0)
            self.toolbar.add(vbox)
            separator = gtk.VSeparator()
            separator.set_size_request(8, 32)
            self.toolbar.add(separator)

        if help == True:
            self.button_help = Buttons.Simple().create(stock_image=gtk.STOCK_HELP, width=-1, height=32)
            self.button_help.connect('clicked', self.on_button_help_clicked)
            self.toolbar.add(self.button_help)

        self.toolbar.show_all()


    def initialize(self, db_table_object=None, definition_lod=None):
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

        self.db_table = db_table_object
        self.db_object = db_table_object.db_object
        
        self.definition_lod = definition_lod
        self.attributes_lod = self.db_table.attributes
            
        result = GTK_Transformations.search_lod(self.attributes_lod, 'is_primary_key', True)
        if result <> None: 
            self.primary_key_column = result['column_name']

        self.Table.initialize(definition_lod=self.definition_lod, attributes_lod=self.attributes_lod)
        
        # Just populate immideately if this is not a child-table of a form!
        if self.parent_form == None:
            self.populate()


    def populate(self, content_lod=None):        
        if self.parent_form <> None and self.parent_form.primary_key <> None:
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
            substitute_lod = self.db_object.select(table_name=referenced_table_name, column_list=populate_from, where='%s = %i' % (referenced_column_name, foreign_key))
            content_dic[column_name] = mask % substitute_lod[0]
        
        
        
class Form:
    def __init__(self, parent_form=None, icon_file=None, title=None, glade_file=None, window_name=None, help_file=None):
        self.parent_form = parent_form
        self.primary_key_column = None
        
        self.icon_file = icon_file
        self.title = title
        self.glade_file = glade_file
        self.window_name = window_name
        self.help_file = help_file
        
        
    def on_button_save_clicked(self, widget=None, data=None):
        self.save_dataset()
        self.window.destroy()


    def on_button_delete_clicked(self, widget=None, data=None):
        self.delete_dataset()


    def on_button_print_clicked(self, widget=None, data=None):
        pass


    def on_button_help_clicked(self, widget=None, data=None):
        if self.help_file <> None:
            self.HTMLhelp.show(self.help_file)


    def on_window_destroy(self, widget=None, data=None):
        if self.portlets_lod <> None:
            for portlet_row in self.portlets_lod:
                dic = portlet_row
                if dic.has_key('portlet'):
                    if dic.has_key('container'):
                        self.wTree.get_widget(dic['container']).remove(dic['portlet'])
        self.update_func()


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
        
        self.primary_key = primary_key

        if self.help_file <> None:
            help_button_visible = True

        self.create_toolbar(help=help_button_visible)

        # Get wTree, initialize form
        self.wTree = Glade.import_tree(self, self.glade_file, self.window_name)
        self.Form = DataViews.Form(self.wTree)
        self.Form.initialize(definition_lod=self.definition_lod, 
                             attributes_lod=self.attributes_lod)
        self.definition_lod = self.Form.definition_lod

        # Cut form_portlet out of wTree
        glade_window = self.wTree.get_widget(self.window_name)
        self.portlet = glade_window.get_child()
        glade_window.remove(self.portlet)
        glade_window.destroy()

        Window = Containers.Window(icon_file=self.icon_file, title=self.title)
        self.window = Window.create()
        self.window.connect('destroy', self.on_window_destroy)

        self.vbox = gtk.VBox()
        self.window.add(self.vbox)

        self.statusbar = gtk.Statusbar()

        self.vbox.pack_start(self.toolbar, expand=False, fill=True, padding=0)
        self.vbox.pack_start(self.portlet, expand=True, fill=True, padding=0)
        self.vbox.pack_start(self.statusbar, expand=False, fill=True, padding=0)
        
        # Get the portlet_objects and pack them into their container.
        if self.portlets_lod <> None:
            for portlet_row in self.portlets_lod:
                dic = portlet_row
                if dic.has_key('portlet'):
                    if dic.has_key('container'):
                        container = self.wTree.get_widget(dic['container'])
                        container.add(dic['portlet'])
                        if dic.has_key('populate_function') and self.primary_key <> None:
                            dic['populate_function']()
                        
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_modal(True)
        self.window.show_all()

        self.DialogBox = Dialogs.Simple(parent=self.window)
        self.HTMLhelp = HelpFile.HTML()

        if self.primary_key == None:
            self.button_delete.set_sensitive(0)
        self.populate()


    def create_toolbar(self, dataset=True, report=True, help=True):
        self.toolbar = gtk.Toolbar()

        if dataset == True:
            self.button_save = Buttons.Simple().create(stock_image=gtk.STOCK_SAVE, height=32)
            self.button_save.connect('clicked', self.on_button_save_clicked)
            self.toolbar.add(self.button_save)
            self.button_delete = Buttons.Simple().create(stock_image=gtk.STOCK_DELETE, height=32)
            self.button_delete.connect('clicked', self.on_button_delete_clicked)
            self.toolbar.add(self.button_delete)
            separator = gtk.VSeparator()
            separator.set_size_request(8, 32)
            self.toolbar.add(separator)

        # Report widgets
        if report == True:
            self.button_print = Buttons.Simple().create(stock_image=gtk.STOCK_PRINT, height=32)
            self.button_print.connect('clicked', self.on_button_print_clicked)
            self.toolbar.add(self.button_print)
            separator = gtk.VSeparator()
            separator.set_size_request(8, 32)
            self.toolbar.add(separator)

        if help == True:
            self.button_help = Buttons.Simple().create(stock_image=gtk.STOCK_HELP, width=-1, height=32)
            self.button_help.connect('clicked', self.on_button_help_clicked)
            self.toolbar.add(self.button_help)

        self.toolbar.show_all()


    def initialize(self, db_table_object=None, definition_lod=None, attributes_lod=None, portlets_lod=None):
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

        self.db_table = db_table_object
        
        self.definition_lod = definition_lod
        self.attributes_lod = attributes_lod
        self.portlets_lod = portlets_lod
        
        result = GTK_Transformations.search_lod(self.attributes_lod, 'is_primary_key', True)
        if result <> None: 
            self.primary_key_column = result['column_name']
                        
                        
    def populate(self):
        if self.primary_key <> None:
            content_lod = self.db_table.db_object.dictresult('''\
SELECT * FROM %s WHERE %s = %s''' % (self.db_table.name, 
                                     self.primary_key_column, 
                                     self.primary_key))
            self.Form.populate(content_dict=content_lod[0])
        
        # Do callbacks for the population of higher-level widgets.
        for definition_dic in self.definition_lod:
            # First, check if there is a referenced table.
            foreign_content_dic = None
            if definition_dic.has_key('referenced_table_name'):
                foreign_key = content_lod[0][definition_dic['column_name']]
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
        except Exception, inst:
            self.DialogBox.show(dialog_type='error', title='Fehler', inst=inst)


    def delete_dataset(self):
        if self.primary_key <> None:
            response = self.DialogBox.show(dialog_type='yesno', title='Frage', text='Soll dieser Datensatz wirklich gelöscht werden?')
            if response == 'YES':
                try:
                    self.db_table.delete(primary_key_column=self.primary_key_column, primary_key=self.primary_key)
                except Exception, inst:
                    self.DialogBox.show(dialog_type='error', inst=inst)
                    
                self.window.destroy()


    def set_update_function(self, update_func):
        ''' This sets the function triggered with saving and closing. '''

        self.update_func = update_func



class Report:
    pass



class Serial:
    def __init__(self):
        self.com_ports = [1, 2, 3, 4, 5, 6, 7, 8]
        
        try:
            import serial
        except:
            raise
            
        self.serial = serial.Serial()
        self.portlet = Portlets.Serial()
        self.portlet.create()
        
        
    def create(self):
        serial_portlet = self.portlet.create()
        
        self.populate()
        return serial_portlet.widget
        
        
    def populate(self):
        self.portlet.comboboxentry_port.populate(self.com_ports)
        self.portlet.comboboxentry_baudrate.populate(self.serial.BAUDRATES)
        self.portlet.comboboxentry_parity.populate(self.serial.PARITIES)
        self.portlet.comboboxentry_stopbits.populate(self.serial.STOPBITS)
        self.portlet.comboboxentry_databits.populate(self.serial.BYTESIZES)
        
        
        