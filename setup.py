# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI setup module, Version 1.0
# by Mark Muzenhardt, published under LGPL-License.
#
# Give "python setup.py bdist_wininst" to make windows installer.
#===============================================================================

import os, sys
from distutils.core import setup
import __init__ #import *

# First, build documentation --------------------------------------------------
pathname = os.getcwd()


if sys.platform == "win32":
    # Catch install-option before this script runs --------------------------------
    if len(sys.argv) == 1:
        sys.argv.append("bdist_wininst")
    
    
try:
    os.chdir(pathname + '\\doc\\')
    os.system('make html')
    os.chdir(pathname)
except Exception, inst:
    print "Documentation build failed!", inst

print dir(__init__)

# Now, run the real setup script ----------------------------------------------
setup(name         = 'BaseUI',
      packages     = ['BaseUI',
					  'BaseUI/gtkApi',
                      'BaseUI/wxApi',
					  'BaseUI/misc',
					  'BaseUI/dbApi',
	                  'BaseUI/doc'],
      
      package_dir  = {'BaseUI': '.',
					  'BaseUI/gtkApi': 'gtkApi',
                      'BaseUI/wxApi': 'wxApi',
					  'BaseUI/misc': 'misc',
					  'BaseUI/dbApi': 'dbApi',
                      'BaseUI/doc': 'doc/build/html'},
                      
      package_data = {'BaseUI/doc': ['*.*',
                                    'module/*.*',
                                    '_static/*.*', 
                                    '_sources/*.*',  
                                    '_sources/module/*.*',
                                    '_sources/gtkApi/*.*',
                                    '_sources/gtkApi/module/*.*',
                                    '_sources/wxApi/*.*',
                                    '_sources/wxApi/module/*.*',
                                    '_sources/dbApi/*.*',
                                    '_sources/dbApi/module/*.*',
                                    '_sources/misc/*.*',
                                    '_sources/misc/module/*.*',]},
                      
      version      = __init__.__version__,
      description  = 'Advanced Database and user interface API',
      license      = 'GPL',
      url          = 'http://baseui.berlios.de',
      author       = __init__.__author__,
      author_email = 'mark.muzenhardt@googlemail.com',
      platforms     = ['win32', 'linux']
      )
