# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wx.DataViews module.
# by Mark Muzenhardt, published under LGPL license.
#===============================================================================

import os
import wx, wx.xrc

from wx.gizmos import TreeListCtrl
from res import IconSet16

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
        self.cursor_change_function = None
        
        self.number_of_columns = 0
        self.sort_column_number = None
        self.sort_ascending = None
        
        self.Bind(wx.EVT_LIST_COL_CLICK, self.on_header_clicked, id = wx.ID_ANY)

        
    def OnCompareItems(self, a, b):
        a_data = self.GetItemText(a, self.sort_column_number).lower()
        b_data = self.GetItemText(b, self.sort_column_number).lower()
        
        if self.sort_ascending == True:
            result = cmp(a_data, b_data)
        else:
            result = cmp(b_data, a_data)
        return result
    
    
    def on_row_activated(self, event=None):
        row_content = self.get_selected_row_content()
        if self.row_activate_function <> None:
            self.row_activate_function(row_content)


    def on_cursor_changed(self, event=None):
        row_content = self.get_selected_row_content()
        if self.cursor_change_function <> None:
            self.cursor_change_function(row_content)
            
            
    def on_header_clicked(self, event=None):
        clicked_column = event.GetColumn()
        self.set_sort_column(column_number=clicked_column)
    
    
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
        
        # Merge definition_lod and attributes_lod together.
        self.definition_lod = merge_two_lods(self.definition_lod, attributes_lod, 'column_name')
        
        # First off, the columns has to be sorted in given order.
        try:
            self.definition_lod.sort(compare_by('column_number'))
        except:
            raise
        
        # Before anything else happens on the treeview, clear it.
        self.clear()
        
        # Make image list to populate them later!
        self.image_list = wx.ImageList(16, 16)
        
        self.ID_LEFT = self.image_list.Add(IconSet16.getleft_16Bitmap())
        self.ID_UP = self.image_list.Add(IconSet16.getup_16Bitmap())
        self.ID_DOWN = self.image_list.Add(IconSet16.getdown_16Bitmap())
        
        self.SetImageList(self.image_list)
        
        # This makes table column-setup.
        column_number = 0
        for column_dict in self.definition_lod:
            column_label = column_dict.get('column_label')
            if column_label == None:
                column_label = column_dict.get('column_name')
                
            visible = column_dict.get('visible')
            if visible <> False:
                visible = True
            
            self.AddColumn(text=column_label, shown=visible)
            
            sortable = column_dict.get('sortable')
            if sortable <> False:
                self.SetColumnImage(column=column_number, image=self.ID_LEFT)
                
            column_number += 1
        self.number_of_columns = column_number
                

    def populate(self, content_lod=None):
        ''' content_lod = [{'id': 1}] '''
        
        # Needed to update after first population.
        self.DeleteRoot()
        
        self.root = self.AddRoot(text='Root')
        for content_dict in content_lod:
            item = self.AppendItem(parent=self.root, text='')
            
            for definition_dict in self.definition_lod: 
                column_number = definition_dict.get('column_number')
                column_name = definition_dict.get('column_name')
                content = content_dict.get(column_name)
                
                if content == None:
                    content = ''
                
                if type(content) <> unicode:
                    content = str(content)
                self.SetItemText(item, content, column_number)
                
                
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


    def set_cursor_change_function(self, cursor_change_function):
        self.cursor_change_function = cursor_change_function
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_cursor_changed,   id=wx.ID_ANY)


    def set_sort_column(self, column_name=None, column_label=None, column_number=None, ascending=None):
        ''' Enables to sort this widget, even from external. '''
        
        old_column_number = self.sort_column_number
        
        if column_number <> None:
            self.sort_column_number = column_number
        if ascending <> None:
            self.sort_ascending = ascending
        
        if old_column_number == self.sort_column_number:
            if self.sort_ascending == None:
                self.sort_ascending = True
            elif self.sort_ascending == True:
                self.sort_ascending = False
            elif self.sort_ascending == False:
                self.sort_ascending = True
        else:
            self.sort_ascending = True
        
        for column in xrange(self.number_of_columns):
            if column <> self.sort_column_number:
                self.SetColumnImage(column=column, image=self.ID_LEFT)
            else:
                if self.sort_ascending == True:
                    self.SetColumnImage(column=column, image=self.ID_DOWN)
                elif self.sort_ascending == False:
                    self.SetColumnImage(column=column, image=self.ID_UP)
                    
        self.SortChildren(self.root)



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
                
            if widget_object.__class__ ==  wx._controls.TextCtrl:
                if widget_content <> '' and widget_content <> None:
                    if type(widget_content) <> unicode:
                        widget_content = str(widget_content)
                    widget_object.SetValue(widget_content.rstrip())
                else:
                    widget_object.SetValue('')
            if widget_object.__class__ ==  wx._controls.ComboBox:
                # For now ok, but later on there has to be some Blackmagic here!
                if widget_content <> '' and widget_content <> None:
                    if type(widget_content) <> unicode:
                        widget_content = str(widget_content)
                    widget_object.SetValue(widget_content.rstrip())
                else:
                    widget_object.SetValue('')
            if widget_object.__class__ ==  wx._controls.CheckBox:
                if widget_content == '1' or \
                   widget_content == 'Y' or \
                   widget_content == True:
                    widget_content = 1
                else:
                    widget_content = 0
                widget_object.SetValue(int(widget_content))


    def clear(self):
        pass


    def get_content(self):
        ''' Returns the filled content_dict (see method 'populate' for
            further description of its data format). '''

        self.content_dict = {}

        for definition_row in enumerate(self.definition_lod):
            row = definition_row[0]
            dic = definition_row[1]

            widget_object = self.definition_lod[row].get('widget_object')
            widget_name = self.definition_lod[row].get('widget_name')
            column_name = self.definition_lod[row].get('column_name')
            data_type = self.definition_lod[row].get('data_type')

            if widget_object == None or \
               column_name == None:
                continue
            
            if widget_object.__class__ ==  wx._controls.TextCtrl:
                widget_content = widget_object.GetValue()
                if widget_content <> '':
                    self.content_dict[column_name] = widget_content
                else:
                    self.content_dict[column_name] = None
            if widget_object.__class__ == wx._controls.ComboBox:
                # TODO: If there is a db-column sub-referenced, there has to be some code for that!
                
                #if dic.has_key('referenced_column_name'):
                #    if selection <> None:
                #        referenced_column_name = dic['referenced_column_name']
                #        widget_content = selection[referenced_column_name]
                #    else:
                #        widget_content = None
                #else:
                widget_content = widget_object.GetValue()
                if widget_content <> '':
                    self.content_dict[column_name] = widget_content
                else:
                    self.content_dict[column_name] = None
            if widget_object.__class__ == wx._controls.CheckBox:
                widget_content = widget_object.GetValue()
                self.content_dict[column_name] = widget_content
            
            # Make usdate from german date
            # TODO: Whats' this shit here?
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

        
        
if __name__ == "__main__":
    dummy = raw_input('press <RETURN> to exit...')
    
    
    