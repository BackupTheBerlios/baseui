# Give "python setup.py bdist_wininst" to make windows installer.

import os, sys
from distutils.core import setup


# First, build documentation --------------------------------------------------
pathname = os.getcwd()

if sys.platform == "win32" and sys.argv[1] == "build":
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
      
      package_dir  = {'BaseUI': 'src',
					  'BaseUI/GTK': 'src/GTK',
					  'BaseUI/Commons': 'src/Commons',
					  'BaseUI/DB': 'src/DB',
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
      url          = 'http://BaseUI.berlios.de',
      author       = 'Mark Muzenhardt',
      author_email = 'mark.muzenhardt@googlemail.com',
      platforms     = ['win32', 'linux']
      )
