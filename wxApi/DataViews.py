# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wx.DataViews module.
# by Mark Muzenhardt, published under LGPL license.
#===============================================================================

import os
import wx, wx.xrc

#from wx.gizmos import TreeListCtrl
from wx.lib.agw import hypertreelist
from res import IconSet16

from pprint import pprint
from Transformations import *
from Widgets import widget_populator, widget_getter


class Tree(hypertreelist.HyperTreeList):
    ''' This is a framework for the famous wxTreeControl. It builds tables
        from JSON-Definitions to make database-tables easy to draw. '''

    def __init__(self, parent=None):
        hypertreelist.HyperTreeList.__init__(self, parent=parent, id=wx.ID_ANY,
                                     agwStyle=(wx.TR_NO_LINES | wx.TR_HIDE_ROOT | wx.TR_FULL_ROW_HIGHLIGHT | wx.TR_NO_BUTTONS))    
    
        
        self.Hide()
        self.row_activate_function = None
        self.row_right_click_function = None
        self.cursor_change_function = None
        
        self.number_of_columns = 0
        self.sort_column_number = None
        self.sort_ascending = None
        self.sort_data_type = None
        
        #print parent
        #self.mouse_position = (0,0)
        
        self.Bind(wx.EVT_LIST_COL_CLICK, self.on_header_clicked, id=wx.ID_ANY)
        #self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_row_left_clicked)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.on_row_right_clicked)
        #self.Bind(wx.EVT_TR)
        #self.Bind(wx.EVT_MOUSE_EVENTS, self.get_mouse_position)
        #self.Hi
        
        
    def OnCompareItems(self, a, b):
        a_data = self.GetItemText(a, self.sort_column_number).lower()
        b_data = self.GetItemText(b, self.sort_column_number).lower()
        
        # TODO: This sucks somewhat without the foggiest notion of the dateformat, which here is DD.MM.YYYY
        if self.sort_data_type == 'date':
            a_datelist = a_data.split('.')
            b_datelist = b_data.split('.')
            a_data = '%s.%s.%s' % (a_datelist[2], a_datelist[1], a_datelist[0])
            b_data = '%s.%s.%s' % (b_datelist[2], b_datelist[1], b_datelist[0])
        
        if self.sort_data_type == 'bool':
            a_data = self.GetItemImage(a, self.sort_column_number)
            b_data = self.GetItemImage(b, self.sort_column_number)
        
        if self.sort_ascending == True:
            result = cmp(a_data, b_data)
        else:
            result = cmp(b_data, a_data)
        return result
    
    
#    def get_mouse_position(self, event=None):
#        self.mouse_position = event.GetPosition()
#        print 'mouse_pos:', self.mouse_position
        
    
   # def on_row_left_clicked(self, event=None):
        
    def on_row_right_clicked(self, event=None):
        item = event.GetItem()
        
        row_content = self.get_selected_row_content(item)
        if self.row_right_click_function <> None:
            self.SelectItem(item)
            self.row_right_click_function(row_content)
            
        
    def on_row_activated(self, event=None):
        row_content = self.get_selected_row_content()
        if self.row_activate_function <> None:
            self.row_activate_function(row_content)
            
    def on_image_clicked(self, event=None):
        print 'image clicked!'
        
        
    def on_cursor_changed(self, event=None):
        row_content = self.get_selected_row_content()
        
        # TODO: This method is ultra-crappy shit!
        coords = self.ScreenToClient(wx.GetMousePosition())
        coords = (coords[0], coords[1] - 20)
        hit_column = self.HitTest(coords)[2]
        
        for definition_dict in self.definition_lod:
            column_number = definition_dict.get('column_number')
            data_type = definition_dict.get('data_type')
            editable = definition_dict.get('editable')
            if column_number == hit_column:
                if data_type == 'bool' and editable == True: 
                    column_name = definition_dict.get('column_name')
                    cell_content = row_content.get(column_name)
                    item = self.GetSelection()
                    content_dict = item.GetData()
                    
                    if cell_content in ['', None, False]:
                        self.SetItemImage(item, self.ID_CHECKED, column_number)
                        content_dict.update({column_name: True})
                    else:
                        self.SetItemImage(item, self.ID_NOTCHECKED, column_number)
                        content_dict.update({column_name: False})
                    item.SetData(content_dict)
                    # break
        
        if self.cursor_change_function <> None:
            self.cursor_change_function(row_content)
            
            
    def on_header_clicked(self, event=None):
        self.get_content()
        
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
            
        content_lod = []
        item = self.GetRootItem()
        while item <> None:
            item = self.GetNext(item)
            if item <> None:
                content_lod.append(self.get_selected_row_content(item))
        return content_lod


    def get_selected_row_content(self, item=None):
        ''' Returns a dictionary which holds the row content like this:
               {'id': 1, 'name': 'Heinz Becker'} '''
        
        if item == None:     
            item = self.GetSelection()
        
        content_dict = item.GetData()
        return content_dict


    def clear(self):
        ''' Just clears the whole content down to an empty table. '''
        
        return

    
    def initialize(self, definition_lod=None, attributes_lod=None):
        ''' Initializes a treeview as table or tree. The definition_lod
            will be merged with the attributes_lod, thus the attributes_lod
            can be already contained in the definition_lod if desired!
    
            definition_lod = [{'column_name': 'id',

                               'column_label': 'Primärschlüssel',

                               'visible': True,
                               'editable': True,
                               'sortable': True,
                               'resizeable': True,
                               'reorderable': True,
                               'width': 175,
                               'dateformat': '%d.%m.%Y}]

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
        self.ID_CHECKED = self.image_list.Add(IconSet16.getchecked_16Bitmap())
        self.ID_NOTCHECKED = self.image_list.Add(IconSet16.getnotchecked_16Bitmap())
        self.ID_FLAGGED = self.image_list.Add(IconSet16.getflagged_16Bitmap())
        self.ID_NOTFLAGGED = self.image_list.Add(IconSet16.getnotflagged_16Bitmap())
        
        self.SetImageList(self.image_list)
        
        self.Bind(wx.EVT_ACTIVATE, self.on_image_clicked)
        #self.Bind(wx.EVT_ACTIVATE, self.on_image_clicked)
        
        column_number = 0
        for column_dict in self.definition_lod:

            column_label = column_dict.get('column_label')
            if column_label == None:
                column_label = column_dict.get('column_name')
                
            visible = column_dict.get('visible')
            if visible <> False:
                visible = True
                self.AddColumn(text=column_label)
                column_dict['column_number'] = column_number
            else:
                continue
                
            #if column_number == 0 and visible == False:
            #    print 'column 0 must be visible at Tree!'
            #    visible = True
            
            sortable = column_dict.get('sortable')
            if sortable <> False:
                self.SetColumnImage(column=column_number, image=self.ID_LEFT)
            
            width = column_dict.get('width')
            if width <> None:
                self.SetColumnWidth(column_number, width)   
            column_number += 1 
        self.number_of_columns = column_number
        #self.SetMainColumn(main_column)
                

    def populate(self, content_lod=None):
        ''' content_lod = [{'id': 1, #bg_colour, #fg_colour}] '''
        
        # Needed to update after first population.
        self.DeleteRoot()
        self.root = self.AddRoot(text='Root')
        
        for content_dict in content_lod:
            item = self.AppendItem(self.root, text='')
            item.SetData(content_dict)
            
            for definition_dict in self.definition_lod: 
                column_number = definition_dict.get('column_number')
                if column_number == None:
                    continue
                
                column_name = definition_dict.get('column_name')
                data_type = definition_dict.get('data_type')
                editable = definition_dict.get('editable')
                widget = definition_dict.get('widget')
                content = content_dict.get(column_name)
                
                if widget <> None:
                    self.SetItemWindow(item, widget, column_number)
            
                if content_dict.get('#bg_colour') <> None:
                    self.SetItemBackgroundColour(item, content_dict.get('#bg_colour'))
                if content_dict.get('#fg_colour') <> None:
                    self.SetItemTextColour(item, content_dict.get('#fg_colour'))
                    
                if content == None:
                    content = ''
                
                #TODO: self.SetColumnEditable(column_number)
                if data_type == 'bool':
                    
                    # Boolean columns need images to go.
                    if content == True:
                        self.SetItemImage(item, self.ID_CHECKED, column_number)
                    elif content == False:
                        self.SetItemImage(item, self.ID_NOTCHECKED, column_number)
                    else:
                        if editable == True: #  and content == None:
                            self.SetItemImage(item, self.ID_NOTCHECKED, column_number)
                else:
                    # For all other data types, just set text.
                    if type(content) <> unicode:
                        content = str(content)
                    #print content
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
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_cursor_changed,      id=wx.ID_ANY)
        #self.Bind(wx.EVT_LEFT_DOWN, self.on_clicked_anywhere, id=wx.ID_ANY)
        

    def set_sort_column(self, column_name=None, column_label=None, column_number=None, ascending=None):
        ''' Enables to sort this widget, even from external. '''
        
        old_column_number = self.sort_column_number
        
        for attributes_dic in self.definition_lod:
            if attributes_dic.get('column_number') == column_number:
                self.sort_data_type = attributes_dic.get('data_type')
                break
                
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
        self.Layout()
        
        parent.SetSize(self.GetSize()) 
        
        self.content_edited = False
        self.definition_lod = None
        self.attributes_lod = None
        self.content_lod = None
        

    def on_widget_changed(self, widget=None, widget_definition_dict=None):
        self.validate_widget(widget_definition_dict)


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

        # Iterate over the definition_lod
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
            
            # Get the widget_objects and pack them into definition_lod.
            if widget_name <> None:
                widget_object = wx.xrc.XRCCTRL(self, widget_name)
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
                try:
                    widget_content = content_dict[column_name]
                except:
                    print content_dict
                    raise
                
                if self.definition_lod[row].has_key('data_type'):
                    data_type = self.definition_lod[row]['data_type']
                else:
                    data_type = None
            else:
                continue

            if widget_object == None:
                continue
            
            widget_populator(widget_object, widget_content)
                                
    
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
            
            self.content_dict[column_name] = widget_getter(widget_object)
        return self.content_dict
    
    
    def get_widget(self, widget_name):
        return wx.xrc.XRCCTRL(self, widget_name)
        

        
if __name__ == "__main__":
    dummy = raw_input('press <RETURN> to exit...')
    
    
    