# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wxApi Images module.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import wx
import wx.lib.wxcairo

import rsvg
import cairo
        

class SVG(wx.Panel):
    def __init__(self, parent, image_path): #, pos=(0,0), size=(1,1)):
        wx.Panel.__init__(self, parent, id = wx.ID_ANY) #, pos = wx.DefaultPosition, size = wx.Size( 200,460 ))
        
        # self.parent = parent
        self.image_path = image_path
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
        
    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.Render(dc)
        

    def Render(self, dc):
        ctx = wx.lib.wxcairo.ContextFromDC(dc)
        
        #ctx.scale(3, 3)
        #ctx.rotate(45)
        #ctx.translate(80, 10)
        #rsvg.set_default_dpi(100)
        
        svg = rsvg.Handle(self.image_path)
        svg.render_cairo(ctx)
        
        
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = wx.Frame(None, id=wx.ID_ANY)
    svg = SVG(frame, 'res/Auge.svg')
    frame.Show()
    app.MainLoop()
    
    
