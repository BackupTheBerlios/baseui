# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.misc.Windows module.
# published under LGPL license by Mark Muzenhardt.
#===============================================================================

import os


def get_volume_serial(drive_letter):
    out = os.popen('vol %s' % drive_letter)
    out_str = out.read()
    out_list = out_str.split(':')
    
    if len(out_list) > 1:
        drive_serial = out_list[2].replace('\n', '').lstrip()
    else:
        drive_serial = ''
    return drive_serial
    


if __name__ == "__main__":
    dl = raw_input('drive letter > ')
    print get_volume_serial(dl)
    raw_input('give <RETURN> to exit...')

