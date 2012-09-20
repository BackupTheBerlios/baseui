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
            self.insert({'_section': section, '_option': option, '_value': value}, 'id')
        else:
            value = result[0].get('_value')
        return value
        
        
    def set_option(self, section, option, value):
        result = self.select(where="_section = '%s' AND _option = '%s'" % (section, option))
        if result <> []:
            self.update({'_value': value}, where="_section = '%s' AND _option = '%s'" % (section, option))
        else:
            self.insert({'_section': section, '_option': option, '_value': value}, 'id')
            
            
    def get_section(self, section, options_dict=None, prefix_section=False):
        ''' Returns a dict containing all options as key and all values as value.
            if options_dict is given, just the containing keys are fetched. If
            the keys are not already in the section, it adds them with the given
            default (if there is any). If prefix_section is True, all keys will
            be prefixed with the section name + underscore (<section>_<option>).'''
        
        section_dict = {}
        
        # If no options_dict is given,simply read all options in the given section.
        if options_dict == None:
            result = self.select(where="_section = '%s'" % section)
            for row in result:
                option = row.get('_option')
                if option == None:
                    continue
                if prefix_section == True:
                    option = '%s_%s' % (section, option)
                value = row.get('_value')
                section_dict[option] = value
            return section_dict
            
        # If options_dict is given for default, return just its keys in a new dict.
        for option in options_dict:
            value = self.get_option(section, option, options_dict[option])
            if prefix_section == True:
                option = '%s_%s' % (section, option)
            section_dict[option] = value
        return section_dict
        
        
    def save_lod(self, content_lod, remove_prefix=False):
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



