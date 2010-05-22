# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI SyncTools module.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import time
import threading

class Timer(threading.Thread):
    def __init__(self, seconds):
        self.runTime = seconds
        threading.Thread.__init__(self)
    def run(self):
        for x in xrange(1,100):
            time.sleep(self.runTime)
            print "unit %i" % x

# This should someday thread a database synchronisation. 
#c = Timer(.25)
#c.start()

#d = Timer(.5)
#d.start()


class helper_table:
    ''' This makes a table feel like a simple txt-file. There is no alternative if a
        database has to store html, xml or json statements!'''

    db_table_text_definition = \
    [
        {'column_name': 'id'  , 'data_type': 'bigint',  'column_label': 'Zeile',  'column_number':    0, 'is_primary_key': True, 'is_nullable': False},
        {'column_name': 'text', 'data_type': 'varchar', 'column_label': 'Option', 'column_number':    1, 'character_maximum_length': 255}
    ]
    
    def __init__(self, helper_database, helper_table_name, source_database, source_table_name):
        self.database = database
        self.table_name = table_name
        
        
