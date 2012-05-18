# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI AppTools module.
# by Mark Muzenhardt, published under LGPL-License.
#===============================================================================

import SQLdb


class IniTable(SQLdb.table):
    ''' The options_table emulates an .ini-File. It makes a given table behave 
        like BaseUI.misc.FileSystem.iniFile and thus, has the same methods. '''
    
    attributes = \
    [
        {'column_name': 'id',           'data_type': 'bigint',    'is_primary_key': True},
        {'column_name': '_section',     'data_type': 'varchar',   'character_maximum_length': 160}, 
        {'column_name': '_option',      'data_type': 'varchar',   'character_maximum_length': 160},
        # Underline added, because MSsql sucks around the word "option"!
        {'column_name': '_value',       'data_type': 'varchar',   'character_maximum_length': 160},
    ]
    
    def __init__(self, db_object, table_name):
        SQLdb.table.__init__(self, db_object, table_name)
        self.check_attributes(self.attributes, add=True)
        
        
    def get_option(self, section, option, default=''):
        value = str(default)
        
        result = self.select(where="_section = '%s' AND _option = '%s'" % (section, option))
        if result == []:
            self.insert('id', {'_section': section, '_option': option, '_value': value})
        else:
            value = result[0].get('_value')
        return value
        
    
    def set_option(self, section, option, value):
        result = self.select(where="_section = '%s' AND _option = '%s'" % (section, option))
        if result <> []:
            self.update({'_value': value}, where="_section = '%s' AND _option = '%s'" % (section, option))
        else:
            self.insert('id', {'_section': section, '_option': option, '_value': value})
    
    
    def get_section(self, section, options_dict):
        section_dict = {}
        
        for option in options_dict:
            value = self.get_option(section, option, options_dict[option])
            section_dict[option] = value
        return section_dict
        
        
    def save_lod(self, content_lod):
        for content_dict in content_lod:
            section = content_dict.get('section')
            option = content_dict.get('option')
            value = content_dict.get('value')
            
            self.set_option(section, option, value)
            print section, option, value
        
        
    def save_section(self, section, options_dict):
        for option in options_dict:
            value = options_dict[option]
            self.set_option(section, option, value)            



