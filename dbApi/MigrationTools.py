# -*- coding: iso-8859-1 -*-

#===============================================================================
# DBapi MigrationTools module.
# by Mark Muzenhardt, published under LGPL-License.
#===============================================================================


def copy_columns(source_table, columns, target_table, id_column='id', distinct_column=None):
    ''' Copys columns with content to another Table while looking up that there are
        no doublettes at distinct_column. '''
        
    pass


def drop_columns(columns):
    ''' Just drops a list of columns in one flow. '''
    
    pass


def move_columns(source_table, columns, fk_column, target_table, id_column='id', distinct_column=None):
    ''' Moves a list of columns to another table while looking up that there are
        no doublettes at distinct_column. Creates a new field at the source table
        which contains the foreign key to the new dataset in the target_table. '''

    pass

