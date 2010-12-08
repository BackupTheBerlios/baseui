import os
import wx

from wx.tools.img2py import *

IGNORES = ['Thumbs.db']


def process(path, set='16', size='16'):
    append_file=False
    file_list = os.listdir(path)
    
    for filename in file_list:
        if filename in IGNORES:
            print '... ignoring %s' % filename
            continue
            
        img2py(image_file=path + filename,
               python_file='../res/IconSet%s.py' % set, 
               append=append_file, 
               compressed=False, 
               maskClr=None, 
               imgName=filename.replace('.png', '_%s' % size), 
               icon=False, 
               catalog=False, 
               functionCompatible=True, 
               functionCompatibile=-1)
               
        if append_file == False:
            append_file = True

            
process(path='../../res/16/',    set='16',    size='16')
process(path='../../res/32/',    set='32',    size='32')
process(path='../../res/flags/', set='Flags', size='16')
process(path='../../res/mini/',  set='Mini',  size='mini')
        
x=raw_input('press <RETURN> to exit...')

