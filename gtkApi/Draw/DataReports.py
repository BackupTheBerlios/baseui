# -*- coding: iso-8859-1 -*-

#===============================================================================
# GTKapi Draw.DataReports module.
# by Mark Muzenhardt, published under GPL-License.
#===============================================================================

import gtk


class Table:
    def __init__(self, sheet_object):
        self.sheet = sheet_object
        self.cairo_context = sheet_object.cairo_context
        self.factor = sheet_object.factor


    def initialize(self, definition_lod=None, attributes_lod=None):
        ''' definition_lod = [{'column_name': 'id',
                                     'data_type': 'bigint',
                                         => Only needed if no attributes_lod given!

                                     'column_label': 'Primärschlüssel',
                                     'column_number': 0,

                                     'visible': True,

                                     *** MESS REPLACE *** => 'editable': True,
                                     *** MESS REPLACE *** => 'sortable': True,
                                     *** MESS REPLACE *** => 'resizeable': True,
                                     *** MESS REPLACE *** => 'reorderable': True}]

            attributes_lod = [{'column_name': 'id'

                               'data_type': 'bigint'
                               'character_maximum_length': = 20
                               'numeric_precision' = 2
                               'numeric_scale' = ?
                               'is_nullable' = True}]'''

        pass


    def populate(self, content_lod):
        ''' content_lod = [{'id': 1}] '''

        pass



class Form:
    def __init__(self, sheet_object):
        self.sheet = sheet_object
        self.cairo_context = sheet_object.cairo_context
        self.factor = sheet_object.factor


    def initialize(self, form_definition_lod=None, attributes_lod=None):
        ''' This initializes the Form. Following Data exchanges are to met:
            All units are millimeters!
            
            form_definition_lod = \
            [
                {'label': 'name', 'text': 'Name', 'x_pos': 30.0, 'y_pos': 30.0, 
                                  'width': 50.0, 'heigth': 5.0,  'font': 'Courier New 10', 
                                  'fg_color': 'black', 'bg_color': 'white'},

                {'data_field': 'person.name',     'x_pos': 30.0, 'y_pos': 30.0, 
                               'width': 50.0, 'heigth': 5.0, 'font': 'Courier New 10', 
                               'fg_color': 'black', 'bg_color': 'white'},
                
                {'line': }
                   ...
                   ...
                   ...
            ]
            
            There can be every primitive which means this is simply a list_of_dictionarys that contains every primitive that has to be drawn on the page!

            This is old mess which is stated already everywhere!
            attributes_lod = [{'column_name': 'id'

                               'data_type': 'bigint'
                               'character_maximum_length': = 20
                               'numeric_precision' = 2
                               'numeric_scale' = ?
                               'is_nullable' = True}] '''

        pass


    def populate(self, form_content_dict=None):
        ''' form_content_dict = {#column_name: #content}
                #column_name = Name of the database field
                #content     = Content of the database field'''

        pass