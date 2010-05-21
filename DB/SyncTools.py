# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI SyncTools module.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================


class helper_table:
    ''' This makes a table feel like a simple txt-file. There is no alternative if a
        database has to store html, xml or json statements!'''

    db_table_text_definition = \
    [
        {'column_name': 'id'  , 'data_type': 'bigint',  'column_label': 'Zeile',  'column_number':    0, 'is_primary_key': True, 'is_nullable': False},
        {'column_name': 'text', 'data_type': 'varchar', 'column_label': 'Option', 'column_number':    1, 'character_maximum_length': 255}
    ]
    
    def __init__(self, database, table_name):
        self.database = database
        self.table_name = table_name
        
        
    