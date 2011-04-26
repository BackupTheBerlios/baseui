# -*- coding: iso-8859-1 -*-

#===============================================================================
# GTKapi Glade module.
# by Mark Muzenhardt, published under LGPL-License.
#===============================================================================

import sys, os
import gtk.glade


def import_tree(foreign, gladefile, gladetree):
    try:
        #if sys.platform.startswith('linux'):
        #    print sys.platform, os.getcwd()
        #    gladefile = gladefile[2:].replace('\\', '/')
        wTree = gtk.glade.XML(gladefile, gladetree)
    except:
        raise

    dic = {}
    for key in dir(foreign.__class__):
        dic[key] = getattr(foreign, key)
    wTree.signal_autoconnect(dic)
    return wTree


