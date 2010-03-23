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
            if attributes_dic.has_key('data_type'):
                data_type = attributes_dic['data_type']
                for content_dic in content_lod:
                    if content_dic.has_key(column_name):
                        content = content_dic[column_name]
    return content_lod


def transform_timestamp(content):
    return content


def transform_bool(content):
    transform_dic = {'f': False,
                     't': True,
                     '0': False,
                     '1': True,
                     0: False,
                     1: True}
    
    if content.lower() in tranform_dic.keys():
        content = transform_dic[content]
    return content


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
    