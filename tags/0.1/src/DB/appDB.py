# -*- coding: iso-8859-1 -*-

#===============================================================================
# DBapi appDB module.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================


class text_table:
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

        
    def write(self, text):
        self.clear()
        line_list = text.split('\n')
        for content in enumerate(line_list):    
            sql_command = "INSERT id, text VALUES (%i, '%s') INTO %s" % (content[0], content[1], self.table_name)
            self.database.cursor.execute(sql_command)
        return
        
        
    def read(self):
        return text

        
    def clear(self):
        self.database.cursor.execute('DELETE * FROM %s' % self.table_name)
        return
        
        
    def search(self, text):
        return

        
    def create(self):
        return



class tree_table:
    ''' This makes a table feel like a tree! '''

    def __init__(self, db_conn, table_name):
        self.db_conn = db_conn
        self.table_name = table_name

        
    def add_child(self, parent_id=None):
        return

        
    def move_item(self, item_id, target_parent_id):
        return

        
    def remove(self, item_id):
        return

        
    def search(self, text):
        return

        
    def create(self):
        return



