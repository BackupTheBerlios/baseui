# -*- coding: iso-8859-1 -*-

#===============================================================================
# DBapi Transformations module.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import datetime

from pprint import pprint


def DataType_to_SQL(data_type, mssql=False, oracle=False, length=40):
    ''' Opposite of other '''

    if data_type == datetime.datetime:
        sql_data_type = 'timestamp'
    elif data_type == datetime.date:
        sql_data_type = 'date'
    elif data_type == datetime.time:
        sql_data_type = 'time'
    elif data_type == str and length <= 255:
        if mssql == True:
            sql_data_type = 'nvarchar'
        else:
            sql_data_type = 'varchar'
    elif data_type == int:
        sql_data_type = 'int'
    elif data_type == long:
        sql_data_type = 'bigint'
    elif data_type == bool:
        sql_data_type = 'boolean'
    elif data_type == float:
        sql_data_type = 'float'
    return sql_data_type


def write_transform(content, engine):
    if content == None:
        new_content = 'NULL'
    elif content == False and engine == 'sqlite':
        new_content = 0
    elif content == True and engine == 'sqlite':
        new_content = 1
    elif type(content) == str or type(content) == unicode:
        new_content = "'%s'" % content.rstrip().replace("'", "''")
    elif type(content) == datetime.datetime:
        new_content = "'%s'" % transform_timestamp(content)
    else:
        new_content = content
    return new_content
    

def normalize_content(attributes_lod, content_lod):
    ''' This converts database dependent things to clear python types. '''
    
    if attributes_lod == None:
        return content_lod
    
    for attributes_dic in attributes_lod:
        if attributes_dic.has_key('column_name'):
            column_name = attributes_dic['column_name']
            if attributes_dic.has_key('data_type'):
                data_type = attributes_dic['data_type']
                for content_dic in content_lod:
                    if content_dic.has_key(column_name):
                        content = content_dic[column_name]
                        if data_type.startswith('bool'):
                            content_dic[column_name] = transform_bool(content)
                        if data_type.lower() == 'datetime':
                            content_dic[column_name] = transform_timestamp(content)
                        if data_type in ['varchar', 'nvarchar', 'char', 'nchar']:
                            content_dic[column_name] = transform_string(content)
    return content_lod


def transform_string(content):
    if content <> None: # and type(content) <> unicode:
        content = content.rstrip()
        try:
            #content = u'%s' % content
            content = content.encode('utf-8') #, 'utf-8')
        except Exception, inst:
            pass
            #print content, str(inst)
        
        
            
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
    

def SQLite_DataTypes(self, data_type):
    dict = \
    {
    'INTEGER': ['INT', 
                'INTEGER', 
                'TINYINT', 
                'SMALLINT', 
                'MEDIUMINT', 
                'BIGINT', 
                'UNSIGNED BIG INT', 
                'INT2', 
                'INT8'],
    'TEXT':    ['CHARACTER',
                'VARCHAR',
                'VARYING CHARACTER'
                'NCHAR'
                'NATIVE CHARACTER'
                'NVARCHAR'
                'TEXT'
                'CLOB'],
    'NONE':    ['BLOB',
                'no datatype specified'],
    'REAL':    ['REAL',
                'DOUBLE',
                'DOUBLE PRECISION',
                'FLOAT'],
    'NUMERIC': ['NUMERIC',
                'DECIMAL',
                'BOOLEAN',
                'DATE',
                'DATETIME',
                'NUMERIC']
    }
    return


def PostgreSQL_DataTypes(self, data_type):
    dict = \
    {'INTEGER': []
    }

    
def MySQL_DataTypes(self, data_type):
    pass
    
    
def Oracle_DataTypes(self, data_type):
    pass
    
    
    
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


