# -*- coding: iso-8859-1 -*-

#===============================================================================
# dbGizmos module.
# by Mark Muzenhardt, published under GPL-License.
#===============================================================================

from misc.FileSystem import iniFile 
from dbApi import SQLdb


class iniFile:
    def __init__(self, ini_path='', standard_dod):
        ''' {'database': {'driver':    'odbc'},
             'user':     {'firstname': 'parker',
                          'lastname':  'lewis}} '''
        
        self.ini_path = ini_path
        
        ini_file = open(self.ini_path, 'r')
        self.content_dod = None
        
        
    def save(self, settings_dod):
        pass
        
        
        
    #def load(self):
    #    pass
        
        
class doc:        
    '''
    
    +-- screen
      +-- containers
        +-- widgets
  
    '''