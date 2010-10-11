# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wx.DataViews module.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import os
import wx, wx.xrc

from wx.gizmos import TreeListCtrl

from pprint import pprint
from Transformations import *

PATH = os.path.dirname(__file__)


class Tree(TreeListCtrl):
    ''' This is a framework for the famous wxTreeControl. It builds tables
        from JSON-Definitions to make database-tables easy to draw. '''

    def __init__(self, parent=None):
        TreeListCtrl.__init__(self, parent=parent, 
                                    style=(wx.TR_HIDE_ROOT |
                                           wx.TR_FULL_ROW_HIGHLIGHT))    
    
        self.Hide()
        self.row_activate_function = None
        self.cursor_changed_function = None
        

    # Events ------------------------------------------------------------------
#    def on_column_toggled(self, renderer=None, row=None, widget=None, col=None):
#        pass


    def on_row_activated(self, event=None):
        row_content = self.get_selected_row_content()
        if self.row_activate_function <> None:
            self.row_activate_function(row_content)


    def on_cursor_changed(self, event=None):
        row_content = self.get_selected_row_content()
        if self.cursor_changed_function <> None:
            self.cursor_changed_function(row_content)
    
    
    # Actions -----------------------------------------------------------------
    def create(self):
        pass


    def set_headers_visible(self, visible=True):
        pass


    def get_content(self):
        ''' Returns the content as list_of_dictionarys, just like the content_lod
            uses at populate. '''
            
        content_lod = None    
        return content_lod


    def get_selected_row_content(self):
        ''' Returns a dictionary which holds the row content like this:
               {'id': 1, 'name': 'Heinz Becker'} '''
               
        item = self.GetSelection()
        content_dict = {}
        for definition_dict in self.definition_lod:
            column_number = definition_dict.get('column_number')
            column_name = definition_dict.get('column_name')
            content = self.GetItemText(item, column_number)
            content_dict[column_name] = content
            
        return content_dict


    def clear(self):
        ''' Just clears the whole content down to an empty tabel. '''
        
        return


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
                                  => #image makes a pixbuf column
                                  => #combobox makes a combobox column
                                  => #progressbar makes a progressbar column
                              'character_maximum_length': = 20
                              'numeric_precision' = 2
                              'numeric_scale' = ?
                              'is_nullable' = True}]'''

        self.definition_lod = definition_lod
        
        #treeview_column_list = []
        #self.type_list = []
        
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
        for column_dict in self.definition_lod:
            column_label = column_dict.get('column_label')
            if column_label == None:
                column_label = column_dict.get('column_name')
            else:
                column_label = unicode(column_label, 'cp1252')
                
            visible = column_dict.get('visible')
            if visible <> False:
                visible = True
            self.AddColumn(text=column_label, shown=visible)


    def populate(self, content_lod=None):
        ''' content_lod = [{'id': 1}] '''
        
        root = self.AddRoot(text='Root')
        for content_dict in content_lod:
            item = self.AppendItem(parent=root, text='')
            
            for definition_dict in self.definition_lod: 
                column_number = definition_dict.get('column_number')
                column_name = definition_dict.get('column_name')
                content = content_dict.get(column_name)
                
                if content == None:
                    content = ''
                
                self.SetItemText(item, str(content), column_number)


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
                        #TODO: Remove that 'NULL' crap after getting it into Transformations!
                        if column_content not in [None, 'NULL']:
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
                    if column_dict['data_type'] == "#image":
                        column_content = gtk.gdk.pixbuf_new_from_file(column_content)
                    if column_dict['data_type'] == "#combobox":
                        print 'column_content', column_content
                else:
                    if column_dict['data_type'] == "bool":
                        column_content = False
                    elif column_dict['data_type'].startswith("int") or \
                         column_dict['data_type'] == "bigint":
                        column_content = 0
                    elif column_dict['data_type'] == "float":
                        column_content = 0.0
                    elif column_dict['data_type'] == "#image":
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
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_row_activated, id=wx.ID_ANY)


    def set_cursor_changed_function(self, cursor_changed_function):
        self.cursor_changed_function = cursor_changed_function
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_cursor_changed,   id=wx.ID_ANY)


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



class Form(wx.Panel):
    ''' If data has to be inserted in a database, a input form is needed. This
        class defines a form from a JSON-Definition for easy access. '''

    def __init__(self, parent, xrc_path, panel_name):
        # Preload a panel to subclass it from this class!
        pre_panel = wx.PrePanel()
        self.xrc_resource = wx.xrc.XmlResource(xrc_path)
        self.xrc_resource.LoadOnPanel(pre_panel, parent, panel_name)
        self.PostCreate(pre_panel)

        self.parent = parent
        self.parent.SetInitialSize()
        self.Layout()
        
        self.content_edited = False
        self.definition_lod = None
        self.attributes_lod = None
        self.content_lod = None
        

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
            
            widget_name = dic.get('widget_name')
            # data_type = dic.get('data_type')

            # Get the widget_objects and pack them into definition_lod.
            if widget_name <> None:
                widget_object = wx.xrc.XRCCTRL(self, widget_name)

                # if widget_name.startswith('entry_'):                    
                #     if data_type == 'date':
                #         widget_object = Entrys.Calendar(entry=self.wTree.get_widget(widget_name))
                #     else:
                #         widget_object = Entrys.Simple(self.wTree.get_widget(widget_name))
                #         widget_object.initialize(self.definition_lod[row])
                # if widget_name.startswith('comboboxentry_'):
                #     widget_object = Entrys.Combobox(self.wTree.get_widget(widget_name))
                # if widget_name.startswith('checkbutton_'):
                #     widget_object = self.wTree.get_widget(widget_name)
                # if widget_name.startswith('textview_'):
                #     widget_object = Widgets.TextView(self.wTree.get_widget(widget_name))
                
                self.definition_lod[row]['widget_object'] = widget_object
            #pprint (self.definition_lod)
            

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
                #print widget_name, widget_content, type(widget_content)
                if widget_content == '1' or \
                   widget_content == 'Y' or \
                   widget_content == True:
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
                if self.definition_lod[row].has_key('data_type'):
                    data_type = self.definition_lod[row]['data_type']
                else:
                    data_type = None
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
                
                if dic.has_key('referenced_column_name'):
                    if selection <> None:
                        referenced_column_name = dic['referenced_column_name']
                        widget_content = selection[referenced_column_name]
                    else:
                        widget_content = None
                else:
                    widget_content = widget_object.get_text()
                
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


        
        # Just for testing purpuoses!
        #print self.entry_log.__class__, 'is the same as', wx._controls.TextCtrl
        #if self.entry_log.__class__ ==  wx._controls.TextCtrl:
        #    print 'is really the same...\n\n\n'

        
        
if __name__ == "__main__":
    x = raw_input('press <RETURN> to exit...')
    
    
    