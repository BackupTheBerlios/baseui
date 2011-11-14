# -*- coding: iso-8859-1 -*-

#===============================================================================
# DBapi Transformations module.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import datetime

from pprint import pprint


class SQLtoPythonTransformer(object):    
    def __init__(self, data_types):
        self.py_data_types = {
            'bool':     self.bool,
            'char':     self.char,
            'varchar':  self.varchar,
            'text':     self.string,
            'integer':  self.integer,
            'bigint':   self.long,
            'float':    self.float,
            'numeric':  self.numeric,
            'date':     self.date,
            'time':     self.time,
            'datetime': self.datetime,
            'blob':     self.string,
            }
        self.db_data_types = data_types
    
    
    def transform_dict(self, content_dict, attributes_dict):
        pass
    
    
    def transform_lod(self, content_lod, attributes_lod):
        pass
    
    
    def bool(self, value, attributes):
        pass
    
    
    def char(self, value, attributes):
        pass
    
    
    def varchar(self, value, attributes):
        pass
    
    
    def integer(self, value, attributes):
        pass
    
    
    def long(self, value, attributes):
        pass
    
    
    def float(self, value, attributes):
        pass
    
    
    def numeric(self, value, attributes):
        pass
    
    
    def date(self, value, attributes):
        pass
    
    
    def time(self, value, attributes):
        pass
    
    
    def datetime(self, value, attributes):
        pass



#def DataType_to_SQL(data_type, mssql=False, oracle=False, length=40):
#    ''' Opposite of other '''
#
#    if data_type == datetime.datetime:
#        sql_data_type = 'datetime'
#    elif data_type == datetime.date:
#        sql_data_type = 'date'
#    elif data_type == datetime.time:
#        sql_data_type = 'time'
#    elif data_type == str and length <= 255:
#        if mssql == True:
#            sql_data_type = 'nvarchar'
#        else:
#            sql_data_type = 'varchar'
#    elif data_type == int:
#        sql_data_type = 'int'
#    elif data_type == long:
#        sql_data_type = 'bigint'
#    elif data_type == bool:
#        sql_data_type = 'boolean'
#    elif data_type == float:
#        sql_data_type = 'float'
#    return sql_data_type


def write_transform(content, engine):
    #print 'WRITE TRANSFORMING', content, type(content)
    if content == None:
        new_content = 'NULL'
    elif content == False and (engine == 'sqlite' or engine == 'odbc'):
        new_content = 0
    elif content == True and (engine == 'sqlite' or engine == 'odbc'):
        new_content = 1
    elif type(content) == str or type(content) == unicode:
        new_content = "'%s'" % content.rstrip().replace("'", "''")
    elif type(content) == datetime.datetime:
        new_content = "'%s'" % transform_timestamp(content)
    else:
        new_content = content
    return new_content
    

def normalize_content(attributes_lod, content_lod, db_object=None):
    ''' This converts database dependent things to clear python types. '''
    
    if db_object <> None:
        encoding = db_object.encoding
        # print db_object, encoding
        
    if attributes_lod == None:
        return content_lod
    
    for attributes_dic in attributes_lod:
        if attributes_dic.has_key('column_name'):
            column_name = attributes_dic['column_name']
            if attributes_dic.has_key('data_type'):
                data_type = attributes_dic['data_type']
                for content_dic in content_lod:
                    if '.' in column_name:
                        # This is needed for foreign columns to appear right!
                        column_name = column_name.split('.')[1]
                    if content_dic.has_key(column_name):
                        content = content_dic[column_name]
                        if data_type.startswith('bool'):
                            content_dic[column_name] = transform_bool(content)
                        if data_type.lower() == 'datetime':
                            pass
                            # Here is an error! If nothing happens, no error occurs!
                            # I think, giving back a datetime object is the right choise!
                            #content_dic[column_name] = transform_timestamp(content)
                            #print 'DEVIL:', content_dic[column_name]
                        if data_type.lower() == 'date':
                            content_dic[column_name] = transform_date(content)
                        if data_type in ['varchar', 'nvarchar', 'char', 'nchar']:
                            content_dic[column_name] = transform_string(content, encoding)
    return content_lod


def transform_string(content, encoding=None):
    if content <> None:
        content = content.rstrip()
        try:
            if encoding <> None:
                content = unicode(content, encoding)
        except Exception, inst:
            print 'encoding:', encoding, 'content:',content, 'type:', type(content)
            raise
    return content
                          

def transform_date(content, strformat='%d.%m.%Y'):
    if type(content) == datetime.datetime or \
       type(content) == datetime.date:
        try:
            content = content.strftime(strformat)
        except Exception, inst:
            print inst
    return content


def transform_timestamp(content, strformat='%d.%m.%y %H:%M:%S'):
    if type(content) == datetime.datetime:
        try:
            content = content.strftime(strformat)
        except Exception, inst:
            print inst
    return content


def transform_bool(content):
    if content == None or type(content) == bool:
        return content
    
    transform_dic = {'f': False,
                     't': True,
                     '0': False,
                     '1': True,
                     0: False,
                     1: True}
    
    if type(content) == str:
        content = content.lower()
        
    if content in transform_dic.keys():
        content = transform_dic[content]
        return content
    else:
        return


def convert_to_sql(attributes_lod, content_lod):
    ''' This converts python data to database dependent datastream. '''
    
    return content_lod
    
    
    
class FieldTransformer:
    ''' This simply puts Data from one key to another.
        definition = \
            {source_column_name: 'firstname', target_column_name: 'Vorname'} '''
            
    def __init__(self):
        pass
    
    
    def translate(self, source_dict, backward=False):
        target_dict = {}
        for source_key in source_dict:
            for translation_dict in self.definition:
                # Swap source and target if backward-flag is True
                if backward == False: 
                    source_column_name = translation_dict['source_column_name']
                    target_column_name = translation_dict['target_column_name']
                else:
                    source_column_name = translation_dict['target_column_name']
                    target_column_name = translation_dict['source_column_name']
                
                # Build target dict on match
                if source_column_name == source_key:
                    target_dict[target_column_name] = source_dict[source_column_name]
        return target_dict
        
    
    def get_target_columns(self):
        target_column_list = []
        for translation_dict in self.definition:
            target_column_list.append(translation_dict['target_column_name'])
        return target_column_list
    
    
    def get_source_columns(self):
        source_column_list = []
        for translation_dict in self.definition:
            source_column_list.append(translation_dict['source_column_name'])
        return source_column_list
    
            
    def build_xml_node(self, target_dict, node_name='', intendation=0):
        intend_str = ''
        for space in xrange(intendation):
            intend_str += ' '
            
        store = intend_str + '<%s>\n' % node_name 

        for key in target_dict:
            if target_dict[key] == None:
                target_dict[key] = ''
            store += intend_str + '    <%s>' % key + target_dict[key] + '</%s>\n' % key

        store += intend_str + '</%s>\n' % node_name
        return store


