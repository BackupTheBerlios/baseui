# -*- coding: iso-8859-1 -*-

#===============================================================================
# DBapi Transformations module.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import datetime


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


def normalize_content(attributes_lod, content_lod):
    ''' This converts database dependent things to clear python types. '''
    
    for attributes_dic in attributes_lod:
        if attributes_dic.has_key('column_name'):
            column_name = attributes_dic['column_name']
            for content_dic in content_lod:
                if content_dic.has_key(column_name):
                    content = content_dic[column_name]
        
                
            
    return content_lod


def convert_to_sql(attributes_lod, content_lod):
    ''' This converts python data to database dependent datastream. '''
    
    return content_lod
    
    