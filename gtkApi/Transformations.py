# -*- coding: iso-8859-1 -*-

#===============================================================================
# GTKapi Transformations module.
# by Mark Muzenhardt, published under LGPL-License.
#===============================================================================

import datetime


def SQL_to_DataType(sql_data_type, datetime_offset=False):
    ''' Returns python data types converted from SQL data type strings.
            sql_data_type = SQL data type as string. '''

    if sql_data_type == 'float' or \
         sql_data_type == 'numeric' or \
         sql_data_type == 'decimal':
        data_type = float
    elif sql_data_type.startswith('int') or \
         sql_data_type.startswith('tinyint') or \
         sql_data_type.startswith('smallint'):
        data_type = int
    elif sql_data_type.startswith('bigint'):
        data_type = long
    elif sql_data_type == 'bit' or \
         sql_data_type.startswith('bool'):
        data_type = bool
    elif sql_data_type == 'datetime' or \
         sql_data_type == 'timestamp':
        if datetime_offset == False:
            data_type = datetime.datetime
        else:
            data_type = str
    elif sql_data_type == 'date':
        if datetime_offset == False:
            data_type = datetime.date
        else:
            data_type = str
    elif sql_data_type == 'time':
        if datetime_offset == False:
            data_type = datetime.time
        else:
            data_type = str
    else:
        data_type = str
    return data_type


def search_lod(lod, key, value):
    for dic in lod:
        if dic.has_key(key):
            if dic[key] == value:
                return dic
    return

    
def filter_lod_for_key(lod, key):
    result_lod = []
    for dic in lod:
        if dic.has_key(key):
            result_lod.append(dic)
    return result_lod
    

def date_to_str(date):
    if date <> None:
        if type(date) == datetime.date:
            year = date.year
            month = date.month
            day = date.day
        else:
            year, month, day = date.split('-')
            year = int(year)
            month = int(month)
            day = int(day)
        date = '%02i.%02i.%04i' % (day, month, year)
    else:
        date = ''
    return date
                            
    
def merge_two_lods(left_lod=None, right_lod=None, matching_key=''):
    ''' Gives back a list_of_dictionarys which is created from merging
        left_lod and right_lod on matching_key (which has to be in both
        list_of_dictionarys). '''

    for left_row in enumerate(left_lod):
        row = left_row[0]
        dic = left_row[1]

        # Melt left_dic and right_dic together.
        if right_lod <> None:
            for right_dic in right_lod:
                if right_dic[matching_key] == dic[matching_key]:
                    left_lod[row].update(right_dic)
    return left_lod


def compare_by(dict_key):
    ''' Called like dict.sort(compare_by(dict_key)), this sorts the dict
        by the values given at dict_key (string which has to be a key in dict). '''
        
    def compare_two_dicts (dict_a, dict_b):
        if dict_a.has_key(dict_key) and dict_b.has_key(dict_key):
            return cmp(dict_a[dict_key], dict_b[dict_key])
        return 0
    return compare_two_dicts


def merge_fields(content, merge_field_list, column_name, separator=', '):
    ''' Adds a column_name key to a content_lod for serializing strings
        contained by merge_field_list, comma separated in this way:
        {'name': 'Foo', 'firstname': 'Bar', column_name: 'Foo, Bar'}
        This is used for combobox_entry_completion things! '''

    if content == None:
        return
        
    input_type = type(content)
    if input_type == dict:
        content = [content]
        
    output = []
    for content_dic in content:
        merged_content = ''
        for merge_field in merge_field_list:
            # Jump to the next field if one has None content!
            if content_dic[merge_field] == None:
                continue
            
            # Merge content together!
            if content_dic.has_key(merge_field):
                if merged_content == '':
                    merged_content += content_dic[merge_field]
                else:
                    merged_content += '%s%s' % (separator, content_dic[merge_field])
        content_dic[column_name] = merged_content
        output.append(content_dic)
    
    if input_type == dict:
        output = output[0]
    return output

