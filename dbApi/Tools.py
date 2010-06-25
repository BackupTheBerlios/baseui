# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.dbApi.Tools module.
# published under BSD license by Mark Muzenhardt.
#===============================================================================

import sys


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

