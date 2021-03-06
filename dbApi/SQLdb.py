# -*- coding: iso-8859-1 -*-

#===============================================================================
# DBapi SQLdb module.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import sys
import Transformations 

from copy import copy
from pprint import pprint


def get_odbc_drivers():
    if sys.platform.startswith('win'):
        import _winreg
        key =  _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\ODBC\\ODBCINST.INI")
        info = _winreg.QueryInfoKey(key)
        
        drivers_list = []
        number_of_keys = info[0]
        for number in xrange(number_of_keys):
            drivers_list.append(unicode(_winreg.EnumKey(key, number), 'latin-1'))
    else:
        drivers_list = []
    return drivers_list
    

def get_engines():
    ''' Returns a list of available database-connectors. '''
    
    engine_list = []
    try:
        import psycopg2
        engine_list.append('PostgreSQL')
    except:
        pass
        
    try:
        import MySQLdb
        engine_list.append('MySQL')
    except:
        pass
    
    try:
        import pymssql
        engine_list.append('MS SQL')
    except:
        pass
    
    try:
        import informixdb
        engine_list.append('Informix')
    except:
        pass
        
    try:
        import cx_Oracle
        engine_list.append('Oracle')
    except:
        pass
    
    try:
        import sqlite3
        engine_list.append('SQLite')
    except:
        pass
    
    try:
        import pyodbc
        engine_list.append('ODBC')
    except:
        pass
    
    try:
        import kinterbasdb
        engine_list.append('Firebird')
    except:
        pass
        
    return sorted(engine_list)



def delegate_object(from_object, into_object):
    ''' This delegates all attributes from_object to into_object. '''
    
    into_arguments = dir(into_object)
    arguments = dir(from_object)
    
    for argument in arguments:
        if not argument.startswith('__') and argument not in into_arguments:
            into_object.__setattr__(argument, from_object.__getattribute__(argument))
            
        

class database(object):
    ''' This class connects SQL databases and unifies the commands to query SQL statements. '''

    def __init__(self, engine='', encoding='cp1252', debug=False):
        ''' Initializes database object by importing db_connector.
                engine = Database to connect (currently MySQL or PostgreSQL). '''
        
        if engine == None:
            engine = ''
        self.engine = engine.lower()
        self.encoding = encoding
        self.debug = debug
        
        __database = None
        if self.engine == 'postgresql':
            __database = postgresql_database(self, self.engine)
        if self.engine == "mysql":
            __database = mysql_database(self)
        if self.engine == "firebird":
            __database = firebird_database(self)
        if self.engine == "informix":
            __database = informix_database(self)
        if self.engine == "mssql":
            __database = mssql_database(self)
        if self.engine == "oracle":
            __database = oracle_database(self)
        if self.engine == "sqlite":
            __database = sqlite_database(self)
        if self.engine == "odbc":
            __database = odbc_generic_database(self)
        
        #TODO: Kick away delegate crap someday. Using a base object is much better!
        if __database <> None:
            delegate_object(__database, self)
        
        
        
class generic_database(object):
    def __init__(self, base_object, engine='', debug=False):
        self.base_object = base_object
        self.engine = engine.lower()
        #self.driver = None
        #self.connection_dict = {}
        self.debug = debug
        
        
    def connect(self, **kwargs):
        self.connection_dict = kwargs
        self.connection = self.connector.connect(database=kwargs['database'], host=kwargs['host'], user=kwargs['user'], password=kwargs['password'])
        self.cursor = self.connection.cursor()
        self.set_arguments(**kwargs)
        return self.connection
        
        
    def close(self):
        ''' Just closes the database connection. '''
        
        if self.debug: print 'closing the database connection and cursor.'
        
        try:
            self.cursor.close()
            self.cursor = None
            
            if self.engine == 'sqlite':
                self.connection.commit()
                
            self.connection.close()
            self.connection = None
        except:
            raise
        return

            
    def set_arguments(self, **kwargs):
        self.name = kwargs.get('database')
        self.driver = kwargs.get('driver')
        delegate_object(self, self.base_object)
        
        
    def drop(self, database):
        ''' Drops the given database and returns the SQLcommand.
            NOTICE: You never can drop the database which is connected! '''
        
        sql_command = "DROP DATABASE %s" % database
        self.cursor.execute(sql_command)
        return sql_command
    

    # Handle SQL commands -----------------------------------------------------
    def commit(self):
        ''' This commit is nessecary for all connectors, that has no autocommit
            such as that for PostgreSQL. '''

        self.cursor.execute("COMMIT")


    def listresult(self, sql_command, fetch=None):
        ''' Executes the given sql_command and gives back a list_of_lists if there
            is more then just one row. Else this just returns a simple list. '''
        
        try:
            if self.debug: print sql_command
            self.cursor.execute(sql_command)
        except:
            print sql_command
            raise
        
        if fetch==None:
            tmp_result = self.cursor.fetchall()
        else:
            tmp_result = self.cursor.fetchmany(fetch)

        outer_list = []
        for outer_item in tmp_result:
            if len(outer_item) > 1:
                inner_list = []
                for inner_item in outer_item:
                    inner_list.append(inner_item)
                outer_list.append(inner_list)
            else:
                outer_list.append(outer_item[0])
        return outer_list


    def dictresult(self, sql_command, fetch=None):
        ''' Executes the given sql_command and gives back a list of dictionarys. 
            Be careful, because the content is untransformed and thus, comes
            a little different from database to database! '''
        
        # cp1252 encoding for proper encoding, don't know exactly why!
        #sql_command = sql_command.encode('cp1252')
        # With ODBCmssql this creates an ugly unicode-error (dunno why again)!
        
        try:
            if self.debug: print sql_command
            self.cursor.execute(sql_command)
        except:
            print sql_command
            raise
        
        if fetch==None:
            lol_result = self.cursor.fetchall()
        else:
            lol_result = self.cursor.fetchmany(fetch)

        lod_result = []
        for row in lol_result:
            tmp = {}
            for idx, col in enumerate(self.cursor.description):
                tmp[col[0]] = row[idx]
            lod_result.append(tmp)
        return lod_result


    def execute(self, sql_command):
        ''' Executes sql_command without returning values (for db-manipulation). '''
        
        if self.debug: print sql_command 
        
        try:
            self.cursor.execute(sql_command)
        except Exception, inst:
            print sql_command
            print str(inst)
            raise
        finally:
            if self.engine in ['mysql', 'psycopg2']:
                self.commit()
        return
        
        
    def dump(self, path='./tmp/', format='csv'):
        if format == 'csv':
            import csv
            
            table_list = self.get_tables()
            print 'dumping as %s, into %s' % (path, format)
            
            for table_name in table_list:
                try:
                    table_object = table(self, table_name)
                except:
                    print 'Error with table %s' % table_name
                    continue
                
                try:
                    content_lod = table_object.get_content()
                    column_list = table_object.get_columns()
                except Exception, inst:
                    print '%s with table %s' % (table_name, str(inst))
                    continue
                
                csv_writer = csv.DictWriter(open(path + table_name + '.csv', 'wb'), fieldnames=column_list)
                
                column_dict = {}
                for column_name in column_list:
                    column_dict[column_name] = column_name
                csv_writer.writerow(column_dict)
                
                for content_dict in content_lod:
                    csv_writer.writerow(content_dict)
                    
                # Memory cleanup, needed for big tables to prevent memory explosion!
                del(content_lod)
                del(column_list)
    
    
    def get_table(self, table_name):
        return table(self, table_name)
        


class sqlite_database(generic_database):
    data_types = {
        'bool':     'CHAR(1)',
        'char':     'CHAR',
        'varchar':  'CHAR',
        'text':     'TEXT',
        'integer':  'INTEGER',
        'bigint':   'INTEGER',
        'float':    'DOUBLE',
        'numeric':  'DOUBLE',
        'date':     'DATE',
        'time':     'TIME',
        'datetime': 'TIMESTAMP',
        'blob':     'BLOB',
        }
        
    def __init__(self, base_object, engine='sqlite'):
        generic_database.__init__(self, base_object, engine)
        
        import sqlite3
        self.connector = sqlite3
        
        
    def connect(self, **kwargs):
        self.connection_dict = kwargs
        self.connection = self.connector.connect(kwargs['filepath'])
        self.cursor = self.connection.cursor()
        self.execute('PRAGMA foreign_keys = ON')
        self.set_arguments(**kwargs)
        return self.connection
        
        
    def execute(self, sql_command):
        # No autocommit on sqlite thus, do it manually!
        super(sqlite_database, self).execute(sql_command)
        self.connection.commit()
        
        
    def get_tables(self):
        ''' Returns a list of table names held by given database. '''

        sqlite_master = self.dictresult('SELECT * FROM sqlite_master;')
        lof_table_names = []

        for dict in sqlite_master:
            if dict['tbl_name'] not in lof_table_names:
                lof_table_names.append(dict['tbl_name'])
        return lof_table_names
        
        
        
class postgresql_database(generic_database):
    data_types = {
        'bool':     'BOOL',
        'char':     'CHAR',
        'varchar':  'VARCHAR',
        'text':     'TEXT',
        'integer':  'INTEGER',
        'float':    'FLOAT8',
        'numeric':  'NUMERIC',
        'date':     'DATE',
        'time':     'TIME',
        'datetime': 'TIMESTAMP',
        'blob':     'BYTEA',
        }
    
    encodings = {'utf8':    'utf-8',
                 'win1252': 'cp1252',
                 'latin1':  'latin-1'}
    
    def __init__(self, base_object, engine='psycopg2'):
        generic_database.__init__(self, base_object, engine)
        
        import psycopg2
        self.connector = psycopg2
        
        
    def connect(self, **kwargs):
        super(postgresql_database, self).connect(**kwargs)
        self.connection.set_isolation_level(self.connector.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        return self.connection
    
    
    def get_tables(self):
        ''' Returns a list of table names held by given database. '''
        
        lof_table_names = self.listresult("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        return lof_table_names
        
        
    def get_users(self):
        ''' Returns a list containing the database users. '''

        # PostgreSQL works like this:
        lod_users = self.dictresult("SELECT * FROM pg_user;")

        # Translate list of lists to simple list
        lof_users = []
        for user in lod_users:
            lof_users.append(user['usename'])
        return lof_users
        
        
    def get_databases(self):
        ''' Returns a list containing all databases available by connected user. '''
        
        lof_databases = self.listresult("SELECT datname FROM pg_database")
        return lof_databases
        
    
    def get_encoding(self):
        encoding = self.listresult('SHOW client_encoding')[0].lower()
        
        if encoding in self.encodings.keys():
            encoding = self.encodings[encoding]
        return encoding
    
    
    def create(self, database, encoding='latin-1'):
        ''' Creates a new, blank database.
                database = Name of the new database.
                encoding = Character-set of the new database:
                    latin1 (Western European).
                    latin2 (Central European).
                    utf8   (Unicode, 8-bit). '''

        sql_command = "CREATE DATABASE " + database
        sql_command += " ENCODING '%s'" % encoding

        try:
            self.cursor.execute(sql_command)
        except:
            raise
        
        
        
class mssql_database(generic_database):
    data_types = {
        'bool':     'BIT',
        'char':     'CHAR',
        'varchar':  'VARCHAR',
        'text':     'TEXT',
        'integer':  'INT',
        'float':    'FLOAT',
        'numeric':  'NUMERIC',
        'date':     'DATETIME',
        'time':     'DATETIME',
        'datetime': 'DATETIME',
        'blob':     'IMAGE',
        }
        
    def __init__(self, base_object, engine='ms sql'):
        generic_database.__init__(self, base_object, engine)
        
        import pymssql
        self.connector = pymssql
    
    
    def get_tables(self):
        ''' Returns a list of table names held by given database. '''

        lof_table_names = self.listresult("SELECT table_name FROM information_schema.tables")
        return lof_table_names
        
        
                    
class mysql_database(generic_database):
    data_types = {
        'boolean':  'BOOL',
        'char':     'CHAR',
        'varchar':  'VARCHAR',
        'text':     'LONGTEXT',
        'integer':  'INT',
        'float':    'DOUBLE',
        'numeric':  'NUMERIC',
        'date':     'DATE',
        'time':     'TIME',
        'datetime': 'DATETIME',
        'blob':     'LONGBLOB',
        }
        
    def __init__(self, base_object, engine='mysql'):
        generic_database.__init__(self, base_object, engine)
        
        import MySQLdb
        self.connector = MySQLdb
        
        
    def connect(self, **kwargs):
        self.connection_dict = kwargs
        self.connection = self.connector.connect(db=kwargs['database'], host=kwargs['host'], user=kwargs['user'], passwd=kwargs['password'])
        self.cursor = self.connection.cursor()
        self.set_arguments(**kwargs)
        return self.connection
        
        
    def get_tables(self):
        ''' Returns a list of table names held by given database. '''

        lof_table_names = self.listresult("SELECT table_name FROM information_schema.tables WHERE table_schema = '%s'" % self.name)
        return lof_table_names
        
        
    def get_users(self):
        ''' Returns a list containing the database users. '''

        lod_users = self.dictresult("SELECT * FROM mysql.user")

        # Translate list of lists to simple list
        lof_users = []
        for user in lod_users:
            if not (user['User'] in lof_users):
                lof_users.append(user['User'])
        return lof_users
        
        
    def create(self, database, encoding='latin-1'):
        ''' Creates a new, blank database.
                database = Name of the new database.
                encoding = Character-set of the new database:
                    latin1 (Western European).
                    latin2 (Central European).
                    utf8   (Unicode, 8-bit). '''

        sql_command = "CREATE DATABASE " + database
        sql_command += " CHARACTER SET '%s'" % encoding

        try:
            self.cursor.execute(sql_command)
        except:
            raise 
        
    
    
class oracle_database(generic_database):
    data_types = {
        'bool':     'CHAR(1)',
        'char':     'CHAR2',
        'varchar':  'VARCHAR2',
        'text':     'CLOB',
        'integer':  'INT',
        'float':    'FLOAT',
        'numeric':  'NUMERIC',
        'date':     'DATE',
        'time':     'CHAR(8)',
        'datetime': 'DATE',
        'blob':     'CLOB',
        }
        
    def __init__(self, base_object, engine='oracle'):
        generic_database.__init__(self, base_object, engine)
        
        import cx_Oracle
        self.connector = cx_Oracle
        
        
        
class firebird_database(generic_database):
    data_types = {
        'bool':     'CHAR(1)',
        'char':     'CHAR',
        'varchar':  'VARCHAR',
        'text':     'BLOB SUB_TYPE 1',
        'integer':  'INTEGER',
        'float':    'DOUBLE PRECISION',
        'numeric':  'DECIMAL(%(precision)s,%(scale)s)',
        'date':     'DATE',
        'time':     'TIME',
        'datetime': 'TIMESTAMP',
        'blob':     'BLOB SUB_TYPE 0',
        }
        
    def __init__(self, base_object, engine='mysql'):
        generic_database.__init__(self, engine)
        
        import kinterbasdb
        self.connector = kinterbasdb
        
        
        
class informix_database(generic_database):
    data_types = {
        'bool':     'CHAR(1)',
        'char':     'CHAR',
        'varchar':  'VARCHAR',
        'text':     'BLOB SUB_TYPE 1',
        'integer':  'INTEGER',
        'float':    'FLOAT',
        'numeric':  'NUMERIC(%(precision)s,%(scale)s)',
        'money':    'FLOAT',
        'date':     'DATE',
        'time':     'CHAR(8)',
        'datetime': 'DATETIME',
        'blob':     'BLOB SUB_TYPE 0',
        }
        
    def __init__(self, base_object, engine='mysql'):
        generic_database.__init__(self, base_object, engine)
        
        import informixdb
        self.connector = informixdb
        
        
    
class db2_database(generic_database):
    data_types = {
        'bool':     'CHAR(1)',
        'char':     'CHAR',
        'varchar':  'VARCHAR',
        'text':     'CLOB',
        'integer':  'INT',
        'float':    'DOUBLE',
        'numeric':  'NUMERIC',
        'money':    'DOUBLE',
        'date':     'DATE',
        'time':     'TIME',
        'datetime': 'TIMESTAMP',
        'blob':     'BLOB',
        }
        
    def __init__(self, base_object, engine='mysql'):
        generic_database.__init__(self, base_object, engine)
        
        # import db2
        # self.connector = db2
        
    
    
class odbc_generic_database(generic_database):
    def __init__(self, base_object, engine='odbc'):
        generic_database.__init__(self, base_object, engine)
        
        import pyodbc
        self.connector = pyodbc
        self.base_object = base_object
    
    
    def connect(self, **kwargs):
        self.connection_dict = kwargs
        
        # This creates the odbc-connection string, which can have different parameters.
        self.connection_string = 'DRIVER={%(driver)s}'
        if kwargs.get('host') not in [None, '']:
            self.connection_string += ';SERVER=%(host)s'
        if kwargs.get('database') not in [None, '']:
            self.connection_string += ';DATABASE=%(database)s'
        if kwargs.get('user') not in [None, '']:
            self.connection_string += ';UID=%(user)s'
        if kwargs.get('password') not in [None, '']:
            self.connection_string += ';PWD=%(password)s'
        if kwargs.get('filepath') not in [None, '']:
            self.connection_string += ';DBQ=%(filepath)s;'
            
        self.connection_string = self.connection_string % kwargs
        self.connection = self.connector.connect(self.connection_string, autocommit=True)
        self.cursor = self.connection.cursor()
        self.set_arguments(**kwargs)
        
        if kwargs.get('driver').lower() == 'sql server':
            __database = odbc_mssql_database(self)
        else: #if '.mdb' in kwargs.get('driver').lower():
            __database = odbc_mssql_database(self)
        
        # Write from selected odbc_class object to self, then write self to database object.
        __super_base_object = self.base_object
        delegate_object(__database, self)
        delegate_object(self, __super_base_object)
        return self.connection
        
        
    def get_connection_string(self):
        return self.connection_string
    
    
    def get_tables(self):
        ''' Returns a list of table names held by given database. '''

        try:
            lof_table_names = self.listresult("SELECT table_name FROM information_schema.tables")
        except Exception, inst:
            print str(inst)
            lof_table_names = []
            for row in self.cursor.tables():
                lof_table_names.append(row.table_name)
        return lof_table_names
    
    
    
class odbc_mssql_database(odbc_generic_database):
    # This works for msSQL, not for others!
    data_types = {
        'bool':     'BIT',
        'char':     'CHAR',
        'varchar':  'VARCHAR',
        'text':     'TEXT',
        'integer':  'INT',
        'bigint':   'BIGINT',
        'float':    'FLOAT',
        'numeric':  'NUMERIC',
        'money':    'FLOAT',
        'date':     'DATETIME',
        'time':     'CHAR(8)',
        'datetime': 'DATETIME',
        'blob':     'IMAGE',
        }
    
#    python_types = {
#        int: ['int', 'tinyint', 'bigint'],
#        str: 
#        }
    def __init__(self, base_object):
        # Write from generic_odbc instance to self to get the cursor etc.
        base_object.base_object.encoding = 'cp1252'
        delegate_object(base_object, self)
        
        
    def decode_error(self, inst):
        inst_str = str(inst)
        start = inst_str[inst_str.rfind(']')+1:]
        error = start[:start.rfind('(')].rstrip()
        return error
        
        
        
# Database Tables --------------------------------------------------------------
class table(object):
    ''' This handles all table-related SQL orders. '''

    def __init__(self, db_object, table_name):
        self.db_object = db_object
        self.name = table_name
        
        engine = self.db_object.engine
        driver = self.db_object.driver
        
        if engine == 'postgresql':
            __table = postgresql_table(self, db_object, table_name)
        if engine == "mysql":
            __table = mysql_table(self, db_object, table_name)
        if engine == "mssql":
            __table = mssql_table(self, db_object, table_name)
        if engine == "oracle":
            __table = oracle_table(self, db_object, table_name)
        if engine == "sqlite":
            __table = sqlite_table(self, db_object, table_name)
        if engine == "odbc":
            __table = odbc_generic_table(self, db_object, table_name)
            if driver <> None:
                if driver.lower() == 'sql server':
                    __table = odbc_mssql_table(self, db_object, table_name)
                    
            
        delegate_object(__table, self)
        
        

class generic_table(object):
    def __init__(self, base_object, db_object, table_name):
        self.base_object = base_object
        self.db_object = db_object
        self.db_cursor = db_object.cursor
        self.name = table_name #.encode('cp1252')
        
        self.primary_key_list = []
        
        
    def _check_alter_column(self):
        pass
    
    
    def _check_delete_column(self):
        pass
    
    
    def _check_add_column(self):
        pass
    
    
    def _after_insert(self, pk):
        pass
    
    
    def _before_update(self, where):
        pass
    
    
    def _after_update(self, content_dict, column_list):
        pass
    
    
    def _before_delete(self, where):
        pass
    
    
    def create(self, attributes_lod = None):
        ''' Creates an empty table in the given database and returnes the SQLcommand.
            attributes_lod is a list of dictionarys with this layout:
                --- Column attributes -----------------------------------------
                column_name              = name of the column.
                data_type                = type of column: varchar, bigint, int, float, date, time, etc.
                character_maximum_length = if data_type = 'varchar', this shows maximum character length.
                numeric_precision        = if data_type = 'float', this shows how precise the values are.
                numeric_scale
                is_nullable              = if nullable, column can be empty.

                --- Reference handling ----------------------------------------
                is_primary_key           = this column is a primary_key.
                referenced_table_name    = foreign table_name which holds the primary_key.
                referenced_column_name   = foreign column_name which holds the primary key.

            if attributes_lod is not given, this function creates a table with one
            primary key column named "id". '''
        
        table_layout = ""
        if attributes_lod == None:
            table_layout += """\
    id bigint PRIMARY KEY """
        else:
            for attribute in attributes_lod:
                referenced_column = column(self, attribute['column_name'])
                attribute_layout  = referenced_column.get_attribute_layout(attribute)

                table_layout += "    "
                table_layout += attribute_layout #attribute['column_name'] + " "
                table_layout += ",\n"
            table_layout = table_layout[0:len(table_layout)-2]
        sql_command = """\
CREATE TABLE """ + self.name + """
(
""" + table_layout + """
)"""
        try:
            self.db_object.execute(sql_command)
        except:
            raise
        return sql_command


    def drop(self):
        ''' Drops a table in the given database and returns the SQLcommand. '''

        sql_command = 'DROP TABLE %s' % self.name
        self.db_object.execute(sql_command)
        return sql_command


    def alter(self, old_attributes_dict, new_attributes_dict):
        # TODO: Override this function from the SQLite-table-class and do it right!
        
        if not 'sqlite' in self.db_object.engine.lower():
            old_column_name = old_attributes_dict.get('column_name')
            
            new_column_name = new_attributes_dict.get('column_name')
            new_data_type = new_attributes_dict.get('data_type')
            new_character_maximum_length = new_attributes_dict.get('character_maximum_length')
            
            if new_character_maximum_length <> None:
                new_character_maximum_length = '(%i)' % new_character_maximum_length
            else:
                new_character_maximum_length = ''
            
            # TODO: Still no numeric-style included!
                
            # TODO: ALTER COLUMN works for MS SQL, perhaps not for other db's (maybe MODIFY COLUMN would be right)!
            sql_command = 'ALTER TABLE %s ALTER COLUMN %s %s%s;' % (self.name, new_column_name, new_data_type, new_character_maximum_length)
            self.db_object.execute(sql_command)
        
        
    def get_attributes(self):
        ''' Gets the table attributes and gives them back as list of dictionarys.
            See function 'create' for key description. '''

        # alternative approach:
#        alt_app = self.select(column_list=['column_name', 
#                                           'data_type', 
#                                           'character_maximum_length'
#                                           'numeric_precision',
#                                           'numeric_scale',
#                                           'is_nullable'], 
#                              where='table_name = %s' % self.name)
#                    
#        print 'Getting alternative attributes:'
#        print '... ' + alt_app
        
#        for attribute in alt_app:
#            if attribute.get('column_name') in primary_key_columns_list:
#                attribute['is_primary_key'] = True
#                
        
        column_name_list              = self.db_object.listresult("SELECT column_name FROM information_schema.columns WHERE table_name = '" + self.name + "'")
        data_type_list                = self.db_object.listresult("SELECT data_type FROM information_schema.columns WHERE table_name = '" + self.name + "';")
        character_maximum_length_list = self.db_object.listresult("SELECT character_maximum_length FROM information_schema.columns WHERE table_name = '" + self.name + "'")
        numeric_precision_list        = self.db_object.listresult("SELECT numeric_precision FROM information_schema.columns WHERE table_name = '" + self.name + "'")
        numeric_scale_list            = self.db_object.listresult("SELECT numeric_scale FROM information_schema.columns WHERE table_name = '" + self.name + "'")
        is_nullable_list              = self.db_object.listresult("SELECT is_nullable FROM information_schema.columns WHERE table_name = '" + self.name + "'")
        
        # Create a list of primary key columns.
        primary_key_columns_list = self.get_primary_key_columns()
        
        attributes_lod = []
        for iter in xrange(len(column_name_list)):
            attributes_dict = {}

            # PostgreSQL returns character varying, MySQL returns varchar.
            if data_type_list[iter] == "character varying":
                data_type_list[iter] = "varchar"

            attributes_dict['column_name'] = column_name_list[iter]
            attributes_dict['data_type']   = data_type_list[iter]
            
            # Only add keys, which are containing data.
            if character_maximum_length_list[iter] <> None:
                attributes_dict['character_maximum_length'] = character_maximum_length_list[iter]
            if numeric_precision_list[iter] <> None:
                attributes_dict['numeric_precision'] = numeric_precision_list[iter]
            if numeric_scale_list[iter] <> None:
                attributes_dict['numeric_scale'] = numeric_scale_list[iter]

            if is_nullable_list[iter] == 'YES':
                attributes_dict['is_nullable'] = True
            if column_name_list[iter] in primary_key_columns_list:
                attributes_dict['is_primary_key'] = True
                self.primary_key_list.append(attributes_dict['column_name'])

            attributes_lod.append(attributes_dict)
        attributes_lod = self.transform_attributes(attributes_lod)
        return attributes_lod
        
        
    def check_attributes(self, attributes_lod, add=False, drop=False, alter=False):
        ''' Returns differences_lod, if attributes_lod differ from the real database table definition.
            See function 'create' for key description of attributes_lod.

            add = If True, add not existing columns to the table.
            drop = If True, drop columns which are in the database but not in attributes_lod.
            alter = If True, try to convert the content with minimum possible data loss.
            '''
        
        self.attributes = attributes_lod
        #self.base_object.attributes = attributes_lod
        #print 'base object of', self.name, 'is', self.base_object
        delegate_object(self, self.base_object)
        
        not_in_database_lod = []
        not_in_definition_lod = []
        
        # First, look up if this table exists in database.
        table_list = self.db_object.get_tables()
        
        if self.name not in table_list:
            if add == True:
                try:
                    self.create(attributes_lod)
                except:
                    raise
        
        # Check correctness of attributes
        if alter == True:
            # print 'alter for table', self.name, 'is switched on!'
            # TODO: Tune alter to do more (f.e. varchar and numeric!).
            db_attributes_lod = self.get_attributes()
            for db_attributes_dict in db_attributes_lod:
                db_column_name = db_attributes_dict.get('column_name')
                db_data_type = db_attributes_dict.get('data_type')
                db_character_maximum_length = db_attributes_dict.get('character_maximum_length')
                for attributes_dict in self.attributes:
                    column_name = attributes_dict.get('column_name')
                    data_type = attributes_dict.get('data_type')
                    data_type = self.db_object.data_types.get(data_type)
                    character_maximum_length = attributes_dict.get('character_maximum_length')
                    if column_name == db_column_name:
                        old_column_dict={'column_name': db_column_name}
                        new_column_dict = {'column_name': column_name, 'data_type': data_type}
                        
                        do_alter = False
                        if data_type <> None:
                            data_type = data_type.lower()
                        if db_data_type <> data_type:    
                            do_alter = True
                        if db_character_maximum_length <> character_maximum_length:
                            new_column_dict['character_maximum_length'] = character_maximum_length
                            if character_maximum_length <> None:
                                do_alter = True
                        
                        if do_alter:
                            self.alter(old_column_dict, new_column_dict)
        
        #-----------------------------------------------------------------------
        # Unicode error is here before here!
        
        # Compare given attributes with attributes in database. To do that, get attributes first.
        database_column_list = self.get_columns()
        #-----------------------------------------------------------------------
    
        for attributes_dic in attributes_lod:
            #print attributes_dic
            column_name = attributes_dic['column_name']
            if column_name not in database_column_list:
                not_in_database_lod.append(attributes_dic)                           
        
        # Is there any difference?
        if add == True:
            if len(not_in_database_lod) > 0:
                for attributes_dic in not_in_database_lod:
                    new_column = column(self, attributes_dic['column_name'])
                    try:
                        new_column.create(attributes_dic)
                    except:
                        raise
        return not_in_database_lod, not_in_definition_lod
    
    
    def transform_attributes(self, attributes_lod):
        print 'GENERIC DOES NOT TRANSFORM'
        return attributes_lod
        
        
    def get_content(self, fetch=None):
        ''' Fetches all rows and gives them back as list of dictionarys. '''
        
        return self.select(fetch=fetch)
    
    
    def check_content(self, pk_column='', content_lod=[], \
                      check_exclude=[], duplicates_check=[], \
                      add=True, drop=False, update=True):
        
        ''' Checks rows for differences. 
            pk_column is the primary key column in this table.
            content_lod is the content which has to be synchronized with this table.
            check_exclude is a list of fields that will not cause a update, but they are written
                          in case of updating because another field differs.
            duplicates_check is a list of fields that will be checked if already in the table.
                             If just one already existing dataset matches, it will be updated.
                             If more than one datasets match, it will cause an exception.
            add = If True, add not existing rows in content_lod to the table.
            drop = If True, drop rows which are in the table but not in content_lod.
            update = If True, try to update existing rows with the data given in content_lod. '''
        
        if len(content_lod) > 0:
            column_list = content_lod[0].keys()
            
        for content in content_lod:
            result = self.select(column_list=column_list, where = '%s = %i' % (pk_column, content[pk_column]))
            print "checking:", content
            
            if result == []: 
                print 'content:', content, 'not in table!'
                self.insert(content=content)
            else:
                # First, copy content and result
                check_content = copy(content)
                check_result = copy(result[0])
                
                # Check, which columns are to update
                update_columns = [pk_column]
                for content_key in check_content:
                    result_str = check_result.get(content_key)
                    content_str = check_content.get(content_key)
                    if result_str <> content_str and content_key not in check_exclude:
                        print 'column: %s. differs, new data is: %s. old data is: %s' % (content_key, content_str, result_str)
                        update_columns.append(content_key)
                
                # Last but not least, do update.         
                if update_columns <> [pk_column]:
                    # Add for check excluded keys if there is any update.
                    for content_key in check_exclude:
                        update_columns.append(content_key)
                        
                    self.update(pk_column, column_list=update_columns, content_dict=content)        
        return


    def get_last_primary_key(self, primary_key_column=''):
        ''' Returns a value which represents the highest primary key in this table.
            This is needed for auto-incrementing (f.e. on insert). '''

        max_primary_key = self.db_object.listresult('SELECT MAX(%s) FROM %s' % (primary_key_column, self.name))[0]
        if max_primary_key == None:
            max_primary_key = 0
        return max_primary_key

    
    def get_primary_key_columns(self):
        ''' Returns the list of primary keys of this table '''
        
        attributes_lod = self.get_attributes()
        pk_list = []
        for attribute_dict in attributes_lod:
            is_primary_key = attribute_dict.get('is_primary_key')
            if is_primary_key in [1, True]:
                column_name = attribute_dict.get('column_name')
                pk_list.append(column_name)
        return pk_list
    
        
    def get_foreign_key_columns(self):
        ''' Returns a list of dictionarys containing this layout:
                column_name            = name of the column.
                referenced_table_name  = foreign table_name which holds the primary_key.
                referenced_column_name = foreign column_name which holds the primary key. '''

        attributes_lod = self.get_attributes()
        fk_list = []
        for attribute_dict in attributes_lod:
            is_foreign_key = attributes_dict.get('is_foreign_key')
            if is_foreign_key in [1, True]:
                column_name = attribute_dict.get('column_name')
                fk_list.append(column_name)
        return fk_list


    def get_foreign_key_column_name(self, attributes_lod, primary_key_column, referenced_table_name):
        for dic in attributes_lod:
            if dic.has_key('referenced_table_name'):
                if dic['referenced_table_name'] == referenced_table_name:
                    if dic.has_key('referenced_column_name'):
                        if dic['referenced_column_name'] == primary_key_column:
                            return dic['column_name']
        return
                            
        
    def get_columns(self):
        ''' Returns a list of columns contained by this table. '''
        
        if self.db_object.engine <> 'sqlite':
            if self.db_object.engine == 'odbc':
                #---------------------------------------------------------------
                # Unicode error is before here
                # print type(self.name)
                self.name = self.name.encode('cp1252')
                column_attributes = self.db_object.cursor.columns(table=self.name)
                #---------------------------------------------------------------
                column_list = []
                for column in column_attributes:
                    column_list.append(column[3])
            else:
                column_list = self.db_object.listresult(u"SELECT column_name FROM information_schema.columns WHERE table_name = '" + self.name + "'")
        else:
            attributes_lod = self.db_object.dictresult("PRAGMA TABLE_INFO(%s)" % self.name)
            column_list = []
            for attributes_dic in attributes_lod:
                for key in attributes_dic:
                    if key == 'name':
                        column_list.append(attributes_dic[key])
        return column_list
        
        
    def join(self, primary_key_column='', referenced_table_name='', referenced_column_name='', mode='outer', where=''):
        print mode, 'join', self.name, 'where', where
        
        konstrukt = ('referenced_table_name, referenced_column_name, column_name')
        
        
    def select(self, distinct=False, join=[], column_list=[], where='', order_by='', listresult=False, fetch=None):
        ''' SELECT order in SQL with transformation of output to python data types. '''
        
        #print self.name
        #print self.attributes
        
        if distinct == False:
            distinct = ''
        else:
            distinct = 'DISTINCT '
            
        if join == []:
            from_str = self.name.decode('cp1252')
        else:
            from_str = self.name
            for table in join:
                from_str += ', %s' % table
                
        if column_list == []:
            sql_command = 'SELECT %s* FROM %s' % (distinct, from_str)
        else:
            column_list_str = ''
            for column_name in column_list:
                column_list_str += column_name + ', '
            column_list_str = column_list_str[0:len(column_list_str)-2]
            sql_command = 'SELECT %s%s FROM %s' % (distinct, column_list_str, from_str)
            
        if where <> '':
            sql_command += ' WHERE %s' % where
        
        if order_by <> '':
            sql_command += ' ORDER BY %s' % order_by
            
        try:
            if listresult == False:
                content_lod = self.db_object.dictresult(sql_command, fetch)
                if 'attributes' in dir(self):
                    content_lod = Transformations.normalize_content(self.attributes, content_lod, self.db_object)
                else:
                    #print has_attributes
                    # This occurs, if no attributes are initialized for the Table.
                    # The problem here is, that an existing db has already attrs,
                    # Which are not readed and transformed yet! 
                    pass
            else:
                # TODO: Here should be a transformation for LOL and lists, too!
                content_lod = self.db_object.listresult(sql_command, fetch)
        except:
            raise
        return content_lod
    
    
    # Data manipulation -------------------------------------------------------
    def insert(self, content=None, auto_increment_column=''):
        ''' Inserts content in this table, which can be a dictionary or a list
            of dictionarys. Auto_increment_column is the name of the column
            which should be auto-incremented manually and is used, if no 
            database-side-autoincrement is available. If this column is given,
            this function returns the primary key. If not, None is returned.'''

        if not type(auto_increment_column) in [str, None]:
            raise Exception, 'Wrong value for auto_increment_column!'
        
        # If content is a dictionary, pack it into a list to get a lod.
        if type(content) == dict:
            content_lod = [content]
        else:
            content_lod = content
            
        # Iterate the rows and insert it in the table.
        actual_pk = None
        for content_dict in content_lod:
            if auto_increment_column <> '':
                actual_pk = self.get_last_primary_key(primary_key_column=auto_increment_column) + 1
                content_dict[auto_increment_column] = actual_pk
                
            sql_command = 'INSERT INTO %s (\n' % self.name
            column_list = content_dict.keys()
            column_names_list = ''
            column_content_list = ''
            for column_name in column_list:
                if content_dict.has_key(column_name):
                    column_names_list += '    %s,\n' % column_name
                    
                    column_content = Transformations.write_transform(content_dict[column_name], self.db_object.engine)
                    column_content_list += '    %s,\n' % column_content
                    
            column_names_list = column_names_list[0:len(column_names_list)-2]
            column_content_list = column_content_list[0:len(column_content_list)-2]

            sql_command += column_names_list + ')\n' + 'VALUES (\n'
            sql_command += column_content_list + ')'
            
            try:
                self.db_object.execute(sql_command)
                self._after_insert(actual_pk)
            except:
                raise
        return actual_pk


    def update(self, content_dict=None, column_list=None, where=''):
        ''' Updates content in this table.
                key_column         = the name of the key column.
                column_list        = list of column_names which have to be updated. If None,
                                     all values in content_dict are updated!
                content_dict       = Content to insert in form of a list_of_dictionarys or
                                     as a single dictionary, where the dict-keys are the
                                     column-names of the table. '''

        sql_command = 'UPDATE %s SET \n' % self.name
        
        if column_list == None:
            column_list = content_dict.keys()
        if column_list <> []:
            for column_name in column_list:
                if content_dict.has_key(column_name):
                    column_content = Transformations.write_transform(content_dict[column_name], self.db_object.engine)
                    sql_command += '    %s = %s,\n' % (column_name, column_content)
            sql_command = sql_command[0:len(sql_command)-2] + '\n'
        sql_command += 'WHERE %s' % where
        
        try:
            self._before_update(where)
            self.db_object.execute(sql_command)
            self._after_update(content_dict, column_list)
        except:
            raise
        return


    def delete(self, where):
        sql_command = 'DELETE FROM %s WHERE %s' % (self.name, where)
        try:
            self._before_delete(where)
            self.db_object.execute(sql_command)
        except:
            raise
        return
    
    

class sqlite_table(generic_table):
    def __init__(self, base_object, db_object, table_name):
        generic_table.__init__(self, base_object, db_object, table_name)
        
        
    def get_attributes(self):
        ''' Gets the table attributes and gives them back as list of dictionarys.
            See function 'create' for key description. '''

        attributes_lod = self.db_object.dictresult("PRAGMA TABLE_INFO(%s)" % self.name)
        new_attributes_lod = []
        for attributes_dic in attributes_lod:
            new_attributes_dic = {}
            for key in attributes_dic:
                if key == 'name':
                    new_attributes_dic['column_name'] = attributes_dic[key]
                if key == 'notnull':
                    if attributes_dic[key] == 99:
                        new_attributes_dic['is_nullable'] = 0 
                    else:
                        new_attributes_dic['is_nullable'] = 1
                if key == 'pk':
                    new_attributes_dic['is_primary_key'] = attributes_dic[key]
                    self.primary_key_list.append(attributes_dic['name'])
                if key == 'type':
                    data_type = attributes_dic[key]
                    data_types_list = data_type.split(' ')
                    new_attributes_dic['data_type'] = data_types_list[0]
                    if len(data_types_list) == 2:
                        new_attributes_dic['character_maximum_length'] = int(data_types_list[1][1:len(data_types_list[1])-1])
            new_attributes_lod.append(new_attributes_dic)
        return new_attributes_lod
    
    
    def select(self, distinct=False, join=[], column_list=[], where='', order_by='', listresult=False, fetch=None):
        # Bool fields only. True is 0 and False is 1 in SQLite.
        where_replace = \
        [
            {'True': '1'},
            {'False': '0'}
        ]
        for value in where_replace:
            where = where.replace(value.keys()[0], value.get(value.keys()[0]))
            
        content_lod = super(sqlite_table, self).select(distinct, join, column_list, where, order_by, listresult, fetch)
        return content_lod
        
        
class postgresql_table(generic_table):    
    def __init__(self, base_object, db_object, table_name):
        generic_table.__init__(self, base_object, db_object, table_name)
        
        
    def get_primary_key_columns(self):
        ''' Returns a list of all primary key column_names. '''

        sql_command = '''\
SELECT               
  pg_attribute.attname, 
  format_type(pg_attribute.atttypid, pg_attribute.atttypmod) 
FROM pg_index, pg_class, pg_attribute 
WHERE 
  pg_class.oid = '%s'::regclass AND
  indrelid = pg_class.oid AND
  pg_attribute.attrelid = pg_class.oid AND 
  pg_attribute.attnum = any(pg_index.indkey)
  AND indisprimary''' % self.name
        
        pk_columns_list = []
        pk_columns_lod = self.db_object.dictresult(sql_command)
        for pk_columns_dict in pk_columns_lod:
            pk_columns_list.append(pk_columns_dict.get('attname'))
            
        # TODO: Doubt that this works if foreign keys are implemented, see: http://dev.mysql.com/doc/refman/5.0/en/key-column-usage-table.html
        # pk_columns_list = self.db_object.listresult("SELECT column_name FROM information_schema.key_column_usage WHERE table_name = '" + self.name + "'")
        return pk_columns_list       
        
        
        
class mysql_table(generic_table):
    def __init__(self, base_object, db_object, table_name):
        generic_table.__init__(self, base_object, db_object, table_name)

        
     
class odbc_generic_table(generic_table):
    def __init__(self, base_object, db_object, table_name):
        generic_table.__init__(self, base_object, db_object, table_name)
        
        
    def get_attributes(self):
        ''' Gets the table attributes and gives them back as list of dictionarys.
            See function 'create' for key description. '''

        # Create a list of primary key columns.
        primary_key_list = self.get_primary_key_columns()
        
        attributes_lod = []
        for row in self.db_object.cursor.columns(table=self.name):
            attributes_dict = {}
            
            is_nullable = row[17]
            if is_nullable == 'YES':
                is_nullable = True
            else:
                is_nullable = False
                
            attributes_dict['column_name'] = row[3]  
            attributes_dict['data_type'] = row[5] 
            attributes_dict['character_maximum_length'] = row[6]
            attributes_dict['numeric_precision'] = None, #FIXME: This numeric precision is to get.
            attributes_dict['numeric_scale'] = None #FIXME: This numeric scale is to get.
            attributes_dict['is_nullable'] = is_nullable
            
            if row[3] in primary_key_list:
                attributes_dict['is_primary_key'] = True
            
            attributes_lod.append(attributes_dict)
            self.transform_attributes(attributes_lod)
        return attributes_lod
    
    
    def transform_attributes(self, attributes_lod):
        ''' This has to be overridden by the db-specialized classes and is only
            here to prevent errors. '''
        print 'gen odbc transform?'
        return attributes_lod
    
    
    def get_primary_key_columns(self):
        ''' Uses ODBC-driver function primaryKeys
            primaryKeys(table, catalog=None, schema=None) --> Cursor

            Creates a result set of column names that make up the primary key for a table by executing the SQLPrimaryKeys function.

            Each row has the following columns:
            
            0: table_cat
            1: table_schem
            2: table_name
            3: column_name
            4: key_seq
            5: pk_name '''
        
        pk_columns_list = []
        try:
            rows = self.db_object.cursor.primaryKeys(self.name)
            
            for key in rows:
                pk_columns_list.append(key[3])
        except Exception, inst:
            print inst
            
        return pk_columns_list   
           
        

class odbc_mssql_table(odbc_generic_table):
    def __init__(self, base_object, db_object, table_name):
        odbc_generic_table.__init__(self, base_object, db_object, table_name)
        
        
    def transform_attributes(self, attributes_lod):
#        for attribute_dict in attributes_lod:
#            data_type = attributes_dict.get('data_type')
#            # Integer type -----------------------------------------------------
#            if data_type in ['int', 'tinyint']:
#                data_type = 'integer'
#            if data_type in ['nvarchar']:
#                data_type = 'varchar'
#            if data_type in ['bit']:
#                data_type = 'bool'
#            if data_type in ['ntext']:
#                data_type = 'text'
                
        return attributes_lod
        
        
        
class odbc_excel_table(odbc_generic_table):
    def __init__(self, base_object, db_object, table_name):
        odbc_generic_table.__init__(self, base_object, db_object, table_name)
        
        
    def get_content(self):
        ''' Fetches all rows and gives them back as list of dictionarys. '''
        
        sql_command = "SELECT * FROM [%s]"
        
        content_lod = self.db_object.dictresult(sql_command % self.name)
        content_lod = Transformations.normalize_content(self.get_attributes(), content_lod, self.db_object)
        return content_lod
    
        
        
# Database Table Columns -------------------------------------------------------
class column:
    def __init__(self, table_object, column_name, **attributes):
        ''' This initializes a database columns where:
            db_conn = Database connector from class db.
            table_name = String which gives the name of the table. 
            **attributes can be: data_type, character_maximum_length, etc.'''
            
        self.table_object = table_object
        self.db_object = table_object.db_object
        self.db_cursor = table_object.db_cursor
        self.name = column_name


    def check_attributes(self, attributes_dic=None, action=None, add=False, drop=False, convert=False):
        pass
        
        
    def get_attribute_layout(self, attributes_dic = None):
        ''' Returns the SQL code snippet for creating one column. It is needed
            everywhere you have to give column attributes, especially for
            CREATE or ALTER tables and columns. '''

        column_layout = ''
        column_layout += attributes_dic['column_name'] + " "
        
        if attributes_dic.has_key('data_type'):
            data_type_list = self.db_object.data_types.keys()
            if attributes_dic['data_type'] in data_type_list:
                column_layout += self.db_object.data_types[attributes_dic['data_type']]
            else:
                column_layout += attributes_dic['data_type']
            
        if attributes_dic.has_key('character_maximum_length'):
            column_layout += " (" + str(attributes_dic['character_maximum_length']) + ")"
            
        if attributes_dic.has_key('is_nullable'):
            if attributes_dic['is_nullable'] == False:
                column_layout += " NOT NULL"
                
        if attributes_dic.has_key('is_primary_key'):
            if attributes_dic['is_primary_key'] == True:
                column_layout += " PRIMARY KEY"
                
        if attributes_dic.has_key('referenced_table_object'):
            attributes_dic['referenced_table_name'] = attributes_dic.get('referenced_table_object').name
            referenced_table_object = attributes_dic.get('referenced_table_object')
            pk_columns = referenced_table_object.get_primary_key_columns()
            #print referenced_table_object.name, pk_columns
            attributes_dic['referenced_column_name'] = pk_columns[0]
            #print attributes_dic
            
            
        if attributes_dic.has_key('referenced_table_name'):
            if attributes_dic.has_key('referenced_column_name'):
                column_layout += " REFERENCES %(referenced_table_name)s (%(referenced_column_name)s)" % attributes_dic
                referenced_table = table(self.db_object, attributes_dic['referenced_table_name'])
                referenced_table_attributes = [{'column_name': attributes_dic['referenced_column_name'],
                                                'data_type': attributes_dic['data_type'],
                                                'is_primary_key': True}]
                if attributes_dic.has_key('character_maximum_length'):
                    referenced_table_attributes[0]['character_maximum_length'] = attributes_dic['character_maximum_length']
                referenced_table.check_attributes(referenced_table_attributes, add=True)
                
        column_layout = column_layout.rstrip()
        return column_layout


    def create(self, attributes_dic = None):
        ''' Creates an empty table in the given database and returnes the SQLcommand.
            attributes_lod is a list of dictionarys with this layout:
                --- Column attributes -----------------------------------------
                column_name              = name of the column.
                data_type                = type of column: varchar, bigint, int, float, date, time, etc.
                character_maximum_length = if data_type = 'varchar', this shows maximum character length.
                numeric_precision        = if data_type = 'float', this shows how precise the values are.
                numeric_scale
                is_nullable              = if nullable, column can be empty.

                --- Reference handling ----------------------------------------
                is_primary_key           = this column is a primary_key.
                referenced_table_name    = foreign table_name which holds the primary_key.
                referenced_column_name   = foreign column_name which holds the primary key.

            if attributes_lod is not given, this function creates a table with one
            primary key column named "id". '''
        
        column_layout = self.get_attribute_layout(attributes_dic)
        # Does not work for msSQL, check out if it works for other DBs!
        # sql_command = 'ALTER TABLE %s ADD COLUMN %s' % (self.table_object.name, column_layout)
        # Note: Seems to work fine for PostgreSQL
        sql_command = 'ALTER TABLE %s ADD %s' % (self.table_object.name, column_layout)
        
        try:
            self.db_object.execute(sql_command)
        except:
            raise


    def drop(self):
        ''' Drops this column in the Database of the containing table.'''
        
        sql_command = 'DROP COLUMN %s FROM %s;' % (self.name, self.table_object.name)
        try:
            self.db_object.execute(sql_command)
        except:
            raise
        
        
    def alter(self, **arguments):
        #TODO: Alter should be possible on colums, too.
        pprint(arguments)
        
        
    def get_content(self):
        ''' Fetches all rows and gives them back as list. '''
        
        sql_command = 'SELECT %s FROM %s;' % (self.name, self.table_object.name)
        try:
            content = self.db_object.listresult(sql_command)
        except:
            raise
        return content
        
        

# Database Users ---------------------------------------------------------------
class user:
    ''' This handles all user-related SQL orders. '''
    
    def __init__(self, db_object, user_name):
        ''' This initializes a database table where:
                db_object = Database connector from class db.
                user_name = String which gives the name of the user. '''

        self.db_object = db_object
        self.db_cursor = db_object.cursor
        self.name = user_name
        
        
    def create(self, password):
        ''' Creates a user with given password. '''

        self.password = password
        sql_command = "CREATE USER " + self.name + "PASSWORD " + self.password
        return sql_command
        
        
    def drop(self):
        ''' Drops a user in the given database and returns the SQLcommand. '''

        sql_command = "DROP USER %s" % self.name
        self.db_object.execute(sql_command)
        return sql_command
        
        

