# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wxApi Images module.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

from pprint import pprint

import wx
import wx.lib.wxcairo

import rsvg
import cairo
        

class SVG(wx.Panel):
    def __init__(self, parent, image_path): 
        wx.Panel.__init__(self, parent, id = wx.ID_ANY) 
        
        self.image_path = image_path
        self.svg = rsvg.Handle(self.image_path)
        
        x_size = self.svg.get_dimension_data()[2]
        y_size = self.svg.get_dimension_data()[3]
        self.SetSize((x_size, y_size))
        
        print "size: x=%d, y=%d" % (x_size, y_size)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
        
    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.Render(dc)
        

    def Render(self, dc):
        self.ctx = wx.lib.wxcairo.ContextFromDC(dc)
        self.svg.render_cairo(self.ctx)
        
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = wx.Frame(None, id=wx.ID_ANY)
    svg = SVG(frame, 'res/Auge.svg')
    frame.Show()
    app.MainLoop()
    
    
