import os, sys #, imp

#config = imp.load_source('config', '../src/config.py')
pathname = os.getcwd()

if sys.platform == "win32":
    os.system('make html')
    os.system('make latex')
    os.system('make htmlhelp')
    os.chdir(pathname + '\\build\\latex\\')
    os.system('pdflatex "%s Referenz.tex"' % ('BaseUI')) #config.APP_NAME)