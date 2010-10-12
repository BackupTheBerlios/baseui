# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.misc.Windows module.
# published under BSD license by Mark Muzenhardt.
#===============================================================================

# For now, empty... but at least the drive serial getter comes here!

import os


def get_volume_serial(drive_letter):
	out = os.popen('vol %s' % drive_letter)
	out_str = out.read()
	out_list = out_str.split(':')
	drive_serial = out_list[3]
	return drive_serial