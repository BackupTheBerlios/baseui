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
					  'BaseUI/GTK',
					  'BaseUI/Commons',
					  'BaseUI/DB',
	                  'BaseUI/doc'],
      
      package_dir  = {'BaseUI': '.',
					  'BaseUI/GTK': 'GTK',
					  'BaseUI/Commons': 'Commons',
					  'BaseUI/DB': 'DB',
                      'BaseUI/doc': 'doc/build/html'},
                      
      package_data = {'BaseUI/doc': ['*.*',
                                    'module/*.*',
                                    '_static/*.*', 
                                    '_sources/*.*',  
                                    '_sources/module/*.*',
                                    '_sources/GTK/*.*',
                                    '_sources/GTK/module/*.*',
                                    '_sources/DB/*.*',
                                    '_sources/DB/module/*.*',
                                    '_sources/Commons/*.*',
                                    '_sources/Commons/module/*.*',]},
                      
      version      = '0.1',
      description  = 'Advanced Database and user interface API',
      license      = 'BSD',
      url          = 'http://baseui.berlios.de',
      author       = 'Mark Muzenhardt',
      author_email = 'mark.muzenhardt@googlemail.com',
      platforms     = ['win32', 'linux']
      )
