# -*- coding: iso-8859-1 -*-

#===============================================================================
# DBapi SQLdb module.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import Transformations 
   
from copy import copy


def get_engines():
    ''' Returns a list of available database-connectors. '''
    
    engine_list = []
    try:
        import pgdb
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
        engine_list.append('msSQL')
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
    return engine_list



class database:
    ''' This class connects SQL databases and unifies the commands to query SQL statements. '''

    def __init__(self, engine='', encoding="latin-1", debug=False):
        ''' Initializes database object by importing db_connector.
                engine = Database to connect (currently MySQL or PostgreSQL). '''

        self.connection = None
        self.cursor = None
        self.engine = engine.lower()
        self.encoding = encoding
        self.debug = debug
        
        if self.debug == True:
            from pprint import pprint
            
        try:
            connector = None
            
            if self.engine == "postgresql":
                import pgdb
                connector = pgdb
            if self.engine == "mysql":
                import MySQLdb
                connector = MySQLdb
            if self.engine == "mssql":
                import pymssql
                connector = pymssql
            if self.engine == "oracle":
                import cx_Oracle
                connector = cx_Oracle
            if self.engine == "sqlite":
                import sqlite3
                connector = sqlite3
            if self.engine == "odbc":
                import pyodbc
                connector = pyodbc
                
            self.connector = connector
        except:
            raise
        return
    
    
    # Connection handling -----------------------------------------------------
    def connect(self, **kwargs):
        ''' Connects the database and gives back the connector which is used to give SQL commands to the database.
                database = Database name on server (or filesystem if SQLite).
                driver   = Only if database=ODBC, a driver string is needed...
                host     = Hostname of database server (or local path to database if SQLite (f.e. localhost:5432).
                user     = Database user.
                password = Password of given user account. 
                filepath = Filepath if the database exists as file.'''
        
        self.name = kwargs['database']
        self.config = kwargs
        
        try:
            if self.debug:
                print 'Connecting database', self.name, '...',
            # The table_schema points to the location where all informations about the tables of the given database are.
            if self.engine.startswith('postgresql'):
                self.connection = self.connector.connect(database=kwargs['database'], host=kwargs['host'], user=kwargs['user'], password=kwargs['password'])
                self.table_schema = 'public'
            if self.engine.startswith('mysql'):
                self.connection = self.connector.connect(db=kwargs['database'], host=kwargs['host'], user=kwargs['user'], passwd=kwargs['password'])
                self.table_schema = kwargs['database']
            if self.engine.startswith('mssql'):
                self.connection = self.connector.connect(host=kwargs['host'], user=kwargs['user'], password=kwargs['password'], database=kwargs['database'])
                self.table_schema = None
            if self.engine.startswith('oracle'):
                self.connection = self.connector.connect()
                self.table_schema = None
            if self.engine.startswith('sqlite'):
                self.connection = self.connector.connect(kwargs['filepath'])
                self.table_schema = None
            if self.engine.startswith('odbc'):
                # This creates the odbc-connection string, which can have different parameters.
                connection_string = 'DRIVER={%(driver)s}'
                if kwargs.get('host') not in [None, '']:
                    connection_string += ';SERVER=%(host)s'
                if kwargs.get('database') not in [None, '']:
                    connection_string += ';DATABASE=%(database)s'
                if kwargs.get('user') not in [None, '']:
                    connection_string += ';UID=%(user)s'
                if kwargs.get('password') not in [None, '']:
                    connection_string += ';PWD=%(password)s'
                if kwargs.get('filepath') not in [None, '']:
                    connection_string += ';DBQ=%(filepath)s;'
                    
                # connection_string = 'DRIVER={%(driver)s};SERVER=%(host)s;DATABASE=%(database)s;UID=%(user)s;PWD=%(password)s' % kwargs
                connection_string = connection_string % kwargs
                self.table_schema = None
                self.connection = self.connector.connect(connection_string, autocommit=True)
                
            if self.debug:
                print 'Ok.'
        except:
            if self.debug:
                print 'Failed!'
                
            self.connection = None
            raise
        
        if self.connection == None:
            raise Exception, 'Fehler beim verbinden der Datenbank'
        
        self.cursor = self.connection.cursor()
        
        if self.engine.startswith('postgresql'):# or self.engine.startswith('mysql'):
            self.commit()
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


    # Database commands -------------------------------------------------------
    def create(self, database, encoding='latin-1'):
        ''' Creates a new, blank database.
                database = Name of the new database.
                encoding = Character-set of the new database:
                    latin1 (Western European).
                    latin2 (Central European).
                    utf8   (Unicode, 8-bit). '''

        sql_command = "CREATE DATABASE " + database

        # PostgreSQL:
        if self.engine == 'postgresql':
            sql_command += " ENCODING '%s'" % encoding

        # MySQL:
        if self.engine == 'mysql':
            sql_command += " CHARACTER SET '%s'" % encoding

        try:
            self.cursor.execute(sql_command)
        except:
            raise
        return sql_command


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


    def listresult(self, sql_command):
        ''' Executes the given sql_command and gives back a list_of_lists if there
            is more then just one row. Else this just returns a simple list. '''
        
        try:
            if self.debug: print sql_command
            self.cursor.execute(sql_command)
        except:
            raise

        tmp_result = self.cursor.fetchall()

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


    def dictresult(self, sql_command):
        ''' Executes the given sql_command and gives back a list of dictionarys. 
            Be careful, because the content is untransformed and thus, comes
            a little different from database to database! '''
        
        try:
            if self.debug: print sql_command
            self.cursor.execute(sql_command)
        except:
            raise
            
        lol_result = self.cursor.fetchall()

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

            if self.engine == 'mysql':
                self.commit()
        except:
            raise
        return


    # Database information ----------------------------------------------------
    def get_databases(self):
        ''' Returns a list containing all databases available by connected user. '''

        lof_databases = []
        if self.engine.startswith('postgresql'):
            sql_command = "SELECT datname FROM pg_database"

        lof_databases = self.listresult(sql_command)
        return lof_databases


    def get_tables(self):
        ''' Returns a list of table names held by given database. '''

        if self.engine in ['mysql', 'postgresql']:
            lof_table_names = self.listresult("SELECT table_name FROM information_schema.tables WHERE table_schema = '" + self.table_schema + "'")
        if self.engine == 'mssql':
            lof_table_names = self.listresult("SELECT table_name FROM information_schema.tables")
        if self.engine == 'odbc':
            lof_table_names = []
            for row in self.cursor.tables():
                lof_table_names.append(row.table_name)
            return lof_table_names
        if self.engine == 'sqlite':
            sqlite_master = self.dictresult("SELECT * FROM sqlite_master")
            lof_table_names = []

            for dict in sqlite_master:
                if dict['tbl_name'] not in lof_table_names:
                    lof_table_names.append(dict['tbl_name'])
        return lof_table_names


    def get_users(self):
        ''' Returns a list containing the database users. '''

        # PostgreSQL works like this:
        if self.engine.startswith('postgres'):
            lod_users = self.dictresult("SELECT * FROM pg_user")

            # Translate list of lists to simple list
            lof_users = []
            for user in lod_users:
                lof_users.append(user['usename'])

        # MySQL works like that:
        if self.engine.startswith('mysql'):
            lod_users = self.dictresult("SELECT * FROM mysql.user")

            # Translate list of lists to simple list
            lof_users = []
            for user in lod_users:
                if not (user['User'] in lof_users):
                    lof_users.append(user['User'])
        return lof_users
    
    
    
class table:
    ''' This handles all table-related SQL orders. '''

    def __init__(self, db_object, table_name):
        ''' This initializes a database table where:
                db_conn = Database connector from class db.
                table_name = String which gives the name of the table. '''

        self.db_object = db_object
        self.db_cursor = db_object.cursor
        self.name = table_name
        
        self.primary_key_list = []


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

        sql_command = "DROP TABLE %s" % self.name
        self.db_object.execute(sql_command)
        return sql_command


    def get_attributes(self):
        ''' Gets the table attributes and gives them back as list of dictionarys.
            See function 'create' for key description. '''

        if self.db_object.engine == 'sqlite':
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
        return attributes_lod


    def check_attributes(self, attributes_lod, action=None, add=False, drop=False, convert=False):
        ''' Returns differences_lod, if attributes_lod differ from the real database table definition.
            See function 'create' for key description of attributes_lod.

            action: A switch with following possible values:
                analyze = just gives back differences, does nothing else.
                add     = gives back differences and adds only columns that not exist.
                cleanup = adds not existing columns and drops the columns which are not defined but in the database.
                convert = convert already existing columns with minimum possible data loss.
                replace = like before, but drops all columns in the database which are not in attributes_lod. 
                
            add = If True, add not existing columns to the table.
            drop = If True, drop columns which are in the database but not in attributes_lod.
            convert = If True, try to convert the content with minimum possible data loss.
            '''

        if action <> None:
            print 'check_attributes action="%s" (Table %s) is deprecated...' % (action, self.name)
            
        not_in_database_lod = []
        not_in_definition_lod = []

        # First, look up if this table exists in database.
        table_list = self.db_object.get_tables()
        
        if self.name not in table_list:
            if action == 'add' or add == True or \
               action == 'convert' or \
               action == 'replace':
                try:
                    self.create(attributes_lod)
                except:
                    raise

        # Compare given attributes with attributes in database. To do that, get attributes first.
        database_column_list = self.get_columns()
        for attributes_dic in attributes_lod:
            column_name = attributes_dic['column_name']
            if column_name not in database_column_list:
                not_in_database_lod.append(attributes_dic)                                  
        
                
        # Is there any difference?
        if action <> 'analyze' or add == True:
            if len(not_in_database_lod) > 0:
                for attributes_dic in not_in_database_lod:
                    new_column = column(self, attributes_dic['column_name'])
                    try:
                        new_column.create(attributes_dic)
                    except:
                        raise
        return not_in_database_lod, not_in_definition_lod


    def get_content(self):
        ''' Fetches all rows and gives them back as list of dictionarys. '''

        content_lod = self.db_object.dictresult("SELECT * FROM %s" % self.name)
        return content_lod


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


    def get_primary_key_columns(self):
        ''' Returns a list of all primary key column_names. '''

        # TODO: Doubt that this works if foreign keys are implemented, see: http://dev.mysql.com/doc/refman/5.0/en/key-column-usage-table.html
        pk_columns_list = self.db_object.listresult("SELECT column_name FROM information_schema.key_column_usage WHERE table_name = '" + self.name + "'")
        return pk_columns_list


    def get_last_primary_key(self, primary_key_column=''):
        ''' Returns a value which represents the highest primary key in this table.
            This is needed for auto-incrementing (f.e. on insert). '''

        max_primary_key = self.db_object.listresult('SELECT MAX(%s) FROM %s' % (primary_key_column, self.name))[0]
        if max_primary_key == None:
            max_primary_key = 0
        return max_primary_key


    def get_foreign_key_columns(self):
        ''' Returns a list of dictionarys containing this layout:
                column_name            = name of the column.
                referenced_table_name  = foreign table_name which holds the primary_key.
                referenced_column_name = foreign column_name which holds the primary key. '''

        # TODO: Foreign keys are not implemented. DoIt.
        
        print "Foreign keys are not implemented now!"
        fk_columns_list = []
        return fk_columns_list


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
                column_attributes = self.db_object.cursor.columns(table=self.name)
                column_list = []
                for column in column_attributes:
                    column_list.append(column[3])
            else:
                column_list = self.db_object.listresult("SELECT column_name FROM information_schema.columns WHERE table_name = '" + self.name + "'")
        else:
            attributes_lod = self.db_object.dictresult("PRAGMA TABLE_INFO(%s)" % self.name)
            column_list = []
            for attributes_dic in attributes_lod:
                for key in attributes_dic:
                    if key == 'name':
                        column_list.append(attributes_dic[key])
        return column_list


    def get_tree(self, attributes_lod):
        ''' Returns a tree definition. '''
        
        print 'This does not work, right now!'
        referenced_table_lod = []
        
        for attribute_dict in attributes_lod:
            if attribute_dict.has_key('referenced_table_name'):
                referenced_table_lod.append({'referenced_table_name':  attribute_dict['referenced_table_name'], 
                                             'referenced_column_name': attribute_dict['referenced_column_name']})
        
        
    def join(self, primary_key_column='', referenced_table_name='', referenced_column_name='', mode='outer', where=''):
        print mode, 'join', self.name, 'where', where
        
        konstrukt = ('referenced_table_name, referenced_column_name, column_name')
        
        
    def select(self, distinct=False, column_list=[], where='', listresult=False):
        ''' SELECT order in SQL with transformation of output to python data types. '''
            
        if distinct == False:
            distinct = ''
        else:
            distinct = 'DISTINCT '
            
        if column_list == []:
            sql_command = 'SELECT %s* FROM %s' % (distinct, self.name)
        else:
            column_list_str = str(column_list)
            column_list_str = column_list_str[1:len(column_list_str) - 1]
            column_list_str = column_list_str.replace("'", "")
            sql_command = 'SELECT %s%s FROM %s' % (distinct, column_list_str, self.name)
            
        if where <> '':
            sql_command += ' WHERE %s' % where
        
        try:
            if listresult == False:
                content_lod = self.db_object.dictresult(sql_command)     
            else:
                # TODO: Here should be a transformation for LOL and lists, too!
                content_lod = self.db_object.listresult(sql_command)
                return content_lod       
        except:
            raise
            
        content_lod = Transformations.normalize_content(self.get_attributes(), content_lod)
        return content_lod
    
    
    # Data manipulation -------------------------------------------------------
    def insert(self, primary_key_column='', content=None):
        ''' Inserts content in this table.
                content            = Content to insert in form of a list_of_dictionarys or
                                     as a single dictionary, where the dict-keys are the
                                     column-names of the table.
                primary_key_column = Name of the primary_key_column for auto-incrementation. 
                                     If it is not given, there has to be no pk-field in the
                                     target table! '''

        # If content is a dictionary, pack it into a list to get a lod.
        if type(content) == dict:
            content_lod = [content]
        else:
            content_lod = content
            
        # Iterate the rows and insert it in the table.
        for content_dict in content_lod:
            if primary_key_column <> '':
                actual_pk = self.get_last_primary_key(primary_key_column = primary_key_column) + 1
                content_dict[primary_key_column] = actual_pk
                
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
            except:
                raise
        return


    def update(self, primary_key_column='', column_list=None, content_dict=None):
        ''' Updates content in this table.
                primary_key_column = string for primary key column.
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
        sql_command += 'WHERE %s = %s' % (primary_key_column, content_dict[primary_key_column])
        
        try:
            self.db_object.execute(sql_command)
        except:
            raise
        return


    def delete(self, column_name='', value=None):
        sql_command = 'DELETE FROM %s WHERE %s = %s' % (self.name, column_name, value)
        try:
            self.db_object.execute(sql_command)
        except:
            raise
        return



class column:
    def __init__(self, table_object, column_name):
        ''' This initializes a database columns where:
            db_conn = Database connector from class db.
            table_name = String which gives the name of the table. '''

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
            column_layout += attributes_dic['data_type']
        if attributes_dic.has_key('character_maximum_length'):
            column_layout += " (" + str(attributes_dic['character_maximum_length']) + ")"
        if attributes_dic.has_key('is_nullable'):
            if attributes_dic['is_nullable'] == False:
                column_layout += " NOT NULL"
        if attributes_dic.has_key('is_primary_key'):
            if attributes_dic['is_primary_key'] == True:
                column_layout += " PRIMARY KEY"
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
        sql_command = 'ALTER TABLE %s ADD %s' % (self.table_object.name, column_layout)

        try:
            self.db_object.execute(sql_command)
        except:
            raise


    def drop(self):
        pass


    def get_content(self):
        ''' Fetches all rows and gives them back as list. '''

        sql_command = 'SELECT %s FROM %s' % (self.name, self.table_object.name)
        try:
            content = self.db_object.listresult(sql_command)
        except:
            raise
        return content



class row:
    ''' This handles single table-rows. '''
    
    def __init__(self, table_object):
        pass
    
    
    
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



