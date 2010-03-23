# -*- coding: iso-8859-1 -*-

#===============================================================================
# GTKapi DataViews module.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import os
import gtk, gobject
import Glade, Entrys, Widgets

from pprint import pprint
from Transformations import *

PATH = os.path.dirname(__file__)


class Tree:
    ''' This is a framework for the famous pyGTK TreeView. It builds tables
        from JSON-Definitions to make database-tables easy to draw. '''

    def __init__(self, widget=None, encoding='latin-1'):
        self.widget = widget
        self.encoding = encoding
        
        self.sort_column = None
        self.store = None


    # Events ------------------------------------------------------------------
    def on_column_toggled(self, renderer=None, row=None, widget=None, col=None):
        model = widget.get_model()
        model[row][col] = not model[row][col]


    def on_row_activated(self, widget=None, path=None, column=None):
        row_content = self.get_selected_row_content(widget)
        self.row_activate_function(row_content)


    def on_cursor_changed(self, widget=None, path=None, column=None):
        row_content = self.get_selected_row_content(widget)
        self.cursor_changed_function(row_content)


    # Actions -----------------------------------------------------------------
    def create(self):
        self.widget = gtk.TreeView()


    def set_headers_visible(self, visible=True):
        self.widget.set_headers_visible(visible)


    def get_content(self):
        pass


    def get_selected_row_content(self, widget=None):
        ''' Returns a dictionary which holds the row content like this:
               {'id': 1, 'name': 'Heinz Becker'} '''
        
        if widget == None:
            widget=self.widget
            
        selection = widget.get_selection()
        selected_tuple = selection.get_selected()
        model = widget.get_model()

        row_content = {}
        for item in xrange(len(model[selected_tuple[1]])):
            definition_dic = search_lod(self.definition_lod, 'column_number', item)
            cell_content = model.get_value(selected_tuple[1], item)
            row_content[definition_dic['column_name']] = cell_content
        return row_content


    def clear(self):
        number = 1
        while number > 0:
            column = self.widget.get_column(0)
            if column <> None:
                number = self.widget.remove_column(column)
            else:
                number = 0


    def initialize(self, definition_lod=None, attributes_lod=None):
        ''' Initializes a treeview as table or tree. The definition_lod
            will be merged with the attributes_lod, thus the attributes_lod
            can be already contained in the definition_lod if desired!

            IMPORTANT: The definition_lod should never have not-continuing numbers!
                       If this is the case, the function 'get_selected_row_content
                       will not work properly!

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

        treeview_column_list = []
        self.type_list = []

        # Merge definition_lod and attributes_lod together.
        self.definition_lod = merge_two_lods(self.definition_lod, attributes_lod, 'column_name')

        # First off, the columns has to be sorted in given order.
        try:
            self.definition_lod.sort(compare_by('column_number'))
        except:
            raise

        # Before anything else happens on the treeview, clear it.
        self.clear()

        # This makes table column-setup.
        column_number = 0
        for column_dict in self.definition_lod:
            if column_dict.has_key('data_type'):
                # Use SQL data_types except image (this is a Tree-only data_type).
                if column_dict['data_type'] == 'image':
                    entry_type = gtk.gdk.Pixbuf
                else:
                    if column_dict.has_key('referenced_column_name'):
                        entry_type = str
                    else:
                        entry_type = SQL_to_DataType(column_dict['data_type'], datetime_offset=True)
            self.type_list += [entry_type]

            # If no column_label entry is found in column_dict, name it like db_field_name.
            if column_dict.has_key('column_label'):
                column_label = unicode(str(column_dict['column_label']), self.encoding)
            else:
                # column_dict must have the key 'column_name' at least.
                try:
                    column_label = unicode(str(column_dict['column_name']), self.encoding)
                except:
                    raise

            # The next question is, of which type the column should be (Toggle, Pixbuf, Bool).
            if entry_type <> bool and entry_type <> gtk.gdk.Pixbuf:
                cell_renderer_text = gtk.CellRendererText()
                if column_dict.has_key('editable'):
                    cell_renderer_text.set_property('editable', column_dict['editable'])
                treeview_column_list.append(gtk.TreeViewColumn(column_label, cell_renderer_text, text=column_number))
            if entry_type == bool:
                cell_renderer_toggle = gtk.CellRendererToggle()
                if column_dict.has_key('editable'):
                    cell_renderer_toggle.set_property('activatable', column_dict['editable'])
                    cell_renderer_toggle.connect('toggled', self.on_column_toggled, self.widget, column_number)
                treeview_column_list.append(gtk.TreeViewColumn(column_label, cell_renderer_toggle))
                treeview_column_list[column_number].add_attribute(cell_renderer_toggle, "active", column_number)
            if entry_type == gtk.gdk.Pixbuf:
                cell_renderer_pixbuf = gtk.CellRendererPixbuf()
                treeview_column_list.append(gtk.TreeViewColumn(column_label, cell_renderer_pixbuf, pixbuf=column_number))
            self.widget.append_column(treeview_column_list[column_number])

            # Resizeable by default.
            if column_dict.has_key('resizeable'):
                treeview_column_list[column_number].set_resizable(column_dict['resizeable'])
            else:
                treeview_column_list[column_number].set_resizable(True)

            # Expand by default.
            if column_dict.has_key('expand'):
                treeview_column_list[column_number].set_expand(column_dict['expand'])
            else:
                treeview_column_list[column_number].set_expand(True)

            # Sortable by default.
            if column_dict.has_key('sortable'):
                if column_dict['sortable'] == True:
                    treeview_column_list[column_number].set_sort_column_id(column_number)
                    treeview_column_list[column_number].set_sort_indicator(column_number)
            else:
                treeview_column_list[column_number].set_sort_column_id(column_number)
                treeview_column_list[column_number].set_sort_indicator(column_number)

            # Not reorderable by default.
            if column_dict.has_key('reorderable'):
                treeview_column_list[column_number].set_reorderable(column_dict['reorderable'])

            # Visible by gtk default, thus only effective if visible=False.
            if column_dict.has_key('visible'):
                treeview_column_list[column_number].set_visible(column_dict['visible'])

            column_number += 1
        return


    def populate(self, content_lod=None):
        ''' content_lod = [{'id': 1}] '''

        # If there is no content, bail out for good.
        if content_lod == None:
            return
            
        self.content_lod = content_lod

        # First, look up content_lod for child nodes.
        self.has_child_node = False
        for row_dict in self.content_lod:
            if row_dict.has_key('#child'):
                self.has_child_node = True

        # Let store be a TreeStore if data has child node(s) or a ListStore if not.
        if self.has_child_node:
            self.store = gtk.TreeStore(*self.type_list)
            self.widget.set_enable_tree_lines(True)
        else:
            self.store = gtk.ListStore(*self.type_list)

        # Build and populate TreeView or ListStore.
        try:
            for row_dict in self.content_lod:
                self.build_store(row_parent=None, row_dict=row_dict)
        except:
            raise

        self.widget.set_model(self.store)
        if self.sort_column <> None:
            self.sort_liststore()
        return


    def build_store(self, row_parent, row_dict):
        row_content = []
        # Read out definition_lod
        for column_dict in self.definition_lod:
            if column_dict.has_key('data_type'):
                if row_dict.has_key(column_dict['column_name']):
                    column_content = row_dict[column_dict['column_name']]
                    
                    if column_dict['data_type'] == "varchar" or \
                       column_dict['data_type'] == "time" or \
                       column_dict['data_type'] == "timestamp" or \
                       column_dict['data_type'] == "text":
                        if column_content <> None:
                            column_content = str(column_content)
                        else:
                            column_content = ''
                    if column_dict['data_type'] == "date":
                        column_content = date_to_str(column_content)
                    if column_dict['data_type'].startswith("int"):
                        if column_content <> None:
                            column_content = int(column_content)
                        else:
                            column_content = 0
                    if column_dict['data_type'] == "float":
                        if column_content <> None:
                            column_content = float(column_content)
                        else:
                            column_content = 0.0
                    if column_dict['data_type'] == "bigint":
                        if column_dict.has_key('referenced_column_name'):
                            column_content = str(column_content)
                        else:
                            if column_content <> None:
                                column_content = long(column_content)
                            else:
                                column_content = 0
                    if column_dict['data_type'] == "bool":
                        if column_content <> None:
                            column_content = int(column_content)
                        else:
                            column_content = 0
                    if column_dict['data_type'] == "image":
                        column_content = gtk.gdk.pixbuf_new_from_file(column_content)
                else:
                    if column_dict['data_type'] == "bool":
                        column_content = False
                    elif column_dict['data_type'].startswith("int") or \
                         column_dict['data_type'] == "bigint":
                        column_content = 0
                    elif column_dict['data_type'] == "float":
                        column_content = 0.0
                    elif column_dict['data_type'] == "image":
                        column_content = gtk.gdk.pixbuf_new_from_file(PATH + "/res/empty_16.png")
                    else:
                        column_content = ""
            else:
                # This means, a column_dict has no key 'data_type'. It is not
                # the worst idea to do absolutely nothing, isn't it?
                pass

            row_content += [column_content]


        if row_dict.has_key('#child'):
            row_parent = self.store.append(row_parent, row_content)
            for node_dict in row_dict['#child']:
                self.build_store(row_parent, node_dict)
        else:
            try:
                if self.has_child_node == False:
                    self.store.append(row_content)
                else:
                    self.store.append(row_parent, row_content)
            except:
                raise


    def build_definition(self, content_lod, column_list=None):
        ''' Returns a definition_lod, which is created from a content_lod lookup.'''

        if column_list == None:
            try:
                column_list = content_lod[1].keys()
            except:
                raise

        definition_lod = []

        for column_number in xrange(len(column_list)):
            column_name = column_list[column_number]

            # If first row should be empty, just make a string-column.
            if content_lod[1].has_key(column_name):
                column_type = type(content_lod[1][column_name])
            else:
                column_type = str

            if column_type == int:
                data_type = 'int'
            elif column_type == long:
                data_type = 'bigint'
            elif column_type == float:
                data_type = 'float'
            else:
                data_type = 'varchar'

            column_label = column_list[column_number]

            definition_lod.append({'column_name': column_name,
                                         'data_type': data_type,
                                         'column_label': column_label,
                                         'column_number': column_number})
        return definition_lod


    def set_row_activate_function(self, row_activate_function):
        self.row_activate_function = row_activate_function
        self.widget.connect('row_activated', self.on_row_activated)


    def set_cursor_changed_function(self, cursor_changed_function):
        self.cursor_changed_function = cursor_changed_function
        self.widget.connect('cursor_changed', self.on_cursor_changed)


    def set_sort_column(self, column_name='', sort_ascending=True):
        ''' Enables the sort-feature for the column given with column_name
            and triggers the sort_liststore function. '''

        definition_dic = search_lod(self.definition_lod, 'column_name', column_name)
        self.sort_column = definition_dic['column_number']
        self.sort_ascending = sort_ascending
        self.sort_liststore()


    def sort_liststore(self): #, column):
        ''' sorts the entire liststore with following args:
                self.sort_column    = column number to sort
                self.sort_ascending = True: Sort ascending / False: Sort descending '''

        if self.store == None:
            return
        
        if self.sort_ascending == True: algorithm = gtk.SORT_ASCENDING
        if self.sort_ascending == False: algorithm = gtk.SORT_DESCENDING

        self.store.set_default_sort_func(lambda *args: self.sort_column)
        self.store.set_sort_column_id(self.sort_column, algorithm)
        #return column



class Form:
    ''' If data has to be inserted in a database, a input form is needed. This
        class defines a form from a JSON-Definition for easy access. '''

    def __init__(self, wTree=None):
        ''' A Form has no real widget, so the wTree from a glade import is needed. '''

        self.content_edited = False

        self.definition_lod = None
        self.attributes_lod = None
        self.content_lod = None
        self.wTree = wTree


    def on_widget_changed(self, widget=None, widget_definition_dict=None):
        self.validate_widget(widget_definition_dict)

        
    def close(self):
        self.window.destroy()


    def initialize(self, definition_lod=None, attributes_lod=None):
        ''' This initializes the Form. Following Data exchanges are to met:

            definition_lod = [{'column_name': 'id',
                               'widget_name': 'entry_name',
                               'widget_object': gtk.Entry,
                               'validation_function': self.validate,
                               'editable': True}]

            attributes_lod = [{'column_name': 'id'
                               'data_type': 'bigint'
                               'character_maximum_length': = 20
                               'numeric_precision' = 2
                               'numeric_scale' = ?
                               'is_nullable' = True}] '''

        self.definition_lod = definition_lod
        self.attributes_lod = attributes_lod

        # Just bail out for good if no definition_lod is given.
        if self.definition_lod == None:
            return

        # Iterate over the definition_lod --------------------------------
        for definition_row in enumerate(self.definition_lod):
            row = definition_row[0]
            dic = definition_row[1]
            
            # Melt definition_dic and attributes_dic together.
            column_name = dic['column_name']
            
            if self.attributes_lod <> None:
                for attributes_dic in self.attributes_lod:
                    if attributes_dic['column_name'] == column_name:
                        self.definition_lod[row].update(attributes_dic)
            
            if dic.has_key('widget_name'):
                widget_name = dic['widget_name']
            else:
                widget_name = None
            
            if dic.has_key('data_type'):
                data_type = dic['data_type']
            else:
                data_type = None
            
            #widget_object = None
            # *** MONKEYPATCH *** MONKEYPATCH *** MONKEYPATCH *** MONKEYPATCH ***
            #setattr(self, self.definition_lod[row]['widget_name'], Entrys.Simple(self.wTree.get_widget(dic['widget_name'])))

            # Get the widget_objects and pack them into definition_lod.
            if widget_name <> None:
                if widget_name.startswith('entry_'):                    
                    if data_type == 'date':
                        widget_object = Entrys.Calendar(entry=self.wTree.get_widget(widget_name))
                    else:
                        widget_object = Entrys.Simple(self.wTree.get_widget(widget_name))
                        widget_object.initialize(self.definition_lod[row])
                if widget_name.startswith('comboboxentry_'):
                    widget_object = Entrys.Combobox(self.wTree.get_widget(widget_name))
                if widget_name.startswith('checkbutton_'):
                    widget_object = self.wTree.get_widget(widget_name)
                if widget_name.startswith('textview_'):
                    widget_object = Widgets.TextView(self.wTree.get_widget(widget_name))
                
                self.definition_lod[row]['widget_object'] = widget_object


    def populate(self, content_dict=None):
        ''' content_dict = {#column_name: #content}
                #column_name = Name of the database field
                #content     = Content of the database field'''

        self.content_dict = content_dict

        for definition_row in enumerate(self.definition_lod):
            row = definition_row[0]
            dic = definition_row[1]

            if dic.has_key('widget_name') and \
               dic.has_key('widget_object'):
                widget_name = self.definition_lod[row]['widget_name']
                widget_object = self.definition_lod[row]['widget_object']
                column_name = self.definition_lod[row]['column_name']
                if self.definition_lod[row].has_key('data_type'):
                    data_type = self.definition_lod[row]['data_type']
                else:
                    data_type = None
            else:
                continue

            if widget_object == None:
                continue

            if content_dict.has_key(column_name):
                widget_content = content_dict[column_name]
                if data_type == 'date':
                    widget_content = date_to_str(widget_content)
            else:
                widget_content = ""

            if widget_name.startswith('entry_') or \
               widget_name.startswith('textview_'):
                if widget_content <> '' and widget_content <> None:
                    widget_object.set_text(str(widget_content).rstrip())
                else:
                    widget_object.set_text('')
            if widget_name.startswith('comboboxentry_'):
                if widget_content <> '' and widget_content <> None:
                    widget_object.set_text(str(widget_content).rstrip())
                else:
                    widget_object.set_text('')
            if widget_name.startswith('checkbutton_'):
                if widget_content == 'Y':
                    widget_content = 1
                else:
                    widget_content = 0
                widget_object.set_active(int(widget_content))


    def clear(self):
        pass


    def get_content(self):
        ''' Returns the filled content_dict (see method 'populate' for
            further description of its data format). '''

        self.content_dict = {}

        for definition_row in enumerate(self.definition_lod):
            row = definition_row[0]
            dic = definition_row[1]

            if dic.has_key('widget_object') and \
               dic.has_key('widget_name'):
                widget_object = self.definition_lod[row]['widget_object']
                widget_name = self.definition_lod[row]['widget_name']
                column_name = self.definition_lod[row]['column_name']
                data_type = self.definition_lod[row]['data_type']
            else:
                continue

            if widget_object == None:
                continue

            if widget_name.startswith('entry_'):
                widget_content = widget_object.get_text()
                if widget_content <> '':
                    self.content_dict[column_name] = widget_content
                else:
                    self.content_dict[column_name] = None
            if widget_name.startswith('comboboxentry_'):
                # Get the selected row (dict)
                selection = widget_object.get_selection()
                print 'selection of', widget_name, ':', selection
                #if dic.has_key('referenced_table_name'):
                #    referenced_table_name = dic['referenced_table_name']
                if dic.has_key('referenced_column_name') and selection <> None:
                    referenced_column_name = dic['referenced_column_name']
                    widget_content = selection[referenced_column_name]
                else:
                    widget_content = widget_object.get_text()
                
               # search_lod(self.attributes_lod, 'referenced_
                
                # Get the key which is referenced (f.e. 'id')
                
                
                #print '... found that:', filter_lod_for_key(self.attributes_lod, 'referenced_column_name', )
                
                # This only, if no foreign_key-relation exists!
                
                
                #-----
                #TODO: Here comes the search of the right scrappy column/value/key!
                #-----
                
               # print 'widget_object.get_selection():\n'
               # pprint (widget_object.get_selection()); print
               # print 'self.attributes_lod:\n'
               # pprint (self.attributes_lod); print
               # print 'self.definition_lod:\n'
               # pprint (self.definition_lod)
                if widget_content <> '':
                    self.content_dict[column_name] = widget_content
                else:
                    self.content_dict[column_name] = None
            if widget_name.startswith('checkbutton_'):
                widget_content = widget_object.get_active()
                self.content_dict[column_name] = widget_content
            if widget_name.startswith('textview_'):
                widget_content = widget_object.get_text()
                self.content_dict[column_name] = widget_content
                #print 'textview_content:', widget_content, widget_object

            # Make usdate from german date
            if data_type == 'date':
                if widget_content <> '':
                    try:
                        day, month, year = widget_content.split('.')
                    except:
                        raise

                    day = int(day)
                    month = int(month)
                    year = int(year)
                    widget_content = '%04i-%02i-%02i' % (year, month, day)
                    self.content_dict[column_name] = widget_content
        return self.content_dict


    def validate_widget(self, widget_definition_dict):
        #TODO: Shut that fuck up!
        validation_function = widget_definition_dict['validation_function']
        widget_name = widget_definition_dict['widget_name']
        widget_content = self.content_dict[widget_name]
        widget_validity = validation_function(widget_content)

        if widget_validity == True:
            pass
        return



class Report:
    ''' Databases are made to print out data. This class does all the messing
        for you and draws the needed report onto a gtk.DrawingArea. '''

    '''
    See Documentation for BRAINWRAPPING.
    '''

