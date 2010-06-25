import os
import wx

from wx.tools.img2py import *

path = '../res/16/'
file_list = os.listdir(path)
append_file = False

for filename in file_list:
    img2py(image_file=path + filename,
           python_file='res/Images.py', 
           append=append_file, 
           compressed=False, 
           maskClr=None, 
           imgName=filename.replace('.png', '_16'), 
           icon=False, 
           catalog=False, 
           functionCompatible=True, 
           functionCompatibile=-1)
           
    if append_file == False:
        append_file = True
        
x=raw_input('press <RETURN> to exit...')

