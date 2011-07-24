# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.ContentDefinitionBase module.
# by Mark Muzenhardt, published under LGPL license.
#===============================================================================

from pprint import pprint


class TableContentBase(object):
    def check_column_substitutions(self):
        ''' Search for one to one relationships in that table and if any there,
            call the do_column_substitutions function and replace them with content. ''' 
        
        for column_dict in self.definition_lod:
            if column_dict.has_key('get_columns'):
                get_columns = column_dict['get_columns']
                if column_dict.has_key('column_name'):
                    column_name = column_dict['column_name']
                    if column_dict.has_key('referenced_table_object'):
                        referenced_table_object = column_dict['referenced_table_object']
                        if column_dict.has_key('referenced_column_name'):
                            referenced_column_name = column_dict['referenced_column_name']
                            self.fill_foreign_columns(column_name, get_columns, referenced_table_object, referenced_column_name)
                            
                            
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
            if column_dic.has_key('sort_from'):
                print column_dic
                print referenced_table_object.select()
                print referenced_table_object.name
            
    
    def fill_foreign_columns(self, column_name, get_columns, referenced_table_object, referenced_column_name):
        for content_dict in self.content_lod:
            foreign_key = content_dict[column_name]
            if foreign_key in [None, 'NULL']:
                continue
            
            foreign_content_dict = referenced_table_object.select(column_list=get_columns, where='%s = %i' % (referenced_column_name, foreign_key))[0]
            foreign_attributes_lod = referenced_table_object.attributes
            
            new_foreign_content_dict = {}
            for key in foreign_content_dict.keys():
                new_key = '%s.%s' % (referenced_table_object.name, key)
                new_foreign_content_dict[new_key] = foreign_content_dict[key]
                for attributes_dict in foreign_attributes_lod:
                    if attributes_dict.get('column_name') == key:
                        attributes_dict['column_name'] = new_key
                        self.attributes_lod.append(attributes_dict)
            content_dict.update(new_foreign_content_dict)
            # pprint(self.attributes_lod)
        
    
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



