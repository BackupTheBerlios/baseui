# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.Commons.Windows module.
# published under BSD license by Mark Muzenhardt.
#===============================================================================


def get_odbc_from_winreg():
    import _winreg
    key =  _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\ODBC\\ODBCINST.INI")
    info = _winreg.QueryInfoKey(key)
    
    drivers_list = []
    number_of_keys = info[0]
    for number in xrange(number_of_keys):
        drivers_list.append(unicode(_winreg.EnumKey(key, number), 'latin-1'))
    return drivers_list

