# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wxApi Images module.
# by Mark Muzenhardt, published under LGPL license.
#===============================================================================

import wx
import xml.etree.cElementTree as etree

from wxpsvg.viewer import RenderPanel
from wxpsvg.svg import document



class Bitmap(wx.Image):
    def __init__(self, file_path=''):
        wx.Image.__init__(self, file_path, wx.BITMAP_TYPE_ANY)
        self.ConvertToBitmap()

    

class SVG(wx.Panel):
    def __init__(self, parent, image_path): 
        wx.Panel.__init__(self, parent, id=wx.ID_ANY) 
        
        self.image_path = image_path
        
        tree = etree.parse(image_path)
        self.document = document.SVGDocument(tree.getroot())
        
        self.sizer = wx.FlexGridSizer()
        self.sizer.AddGrowableRow(0)
        self.sizer.AddGrowableCol(0)
        self.SetSizer(self.sizer)

        
    def Render(self):
        self.render = RenderPanel(self, self.document)
        self.sizer.Add(self.render, 0, wx.ALL|wx.EXPAND)   
        self.Layout()

        

    
