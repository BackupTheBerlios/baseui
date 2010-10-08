# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI setup module.
# by Mark Muzenhardt, published under BSD-License.
#
# Give "python setup.py bdist_wininst" to make windows installer.
#===============================================================================

import os, sys
from distutils.core import setup


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
                      
      version      = '1.1',
      description  = 'Advanced Database and user interface API',
      license      = 'BSD',
      url          = 'http://baseui.berlios.de',
      author       = 'Mark Muzenhardt',
      author_email = 'mark.muzenhardt@googlemail.com',
      platforms     = ['win32', 'linux']
      )
