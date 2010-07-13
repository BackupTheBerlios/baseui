# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wxApi Images module.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import wx

# Here should be asked, if that components are installed!
import wx.lib.wxcairo
import rsvg
import cairo

class TestFrame(wx.Frame):
    def __init__(self, parent, id, title, pos, size):
        wx.Frame.__init__(self, parent, id, title, pos, size)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Show()
        
        
    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.Render(dc)
        

    def Render(self, dc):
        ctx = wx.lib.wxcairo.ContextFromDC(dc)
        rsvg.set_default_dpi(900)
        svg = rsvg.Handle('resources/Auge.svg')
        svg.render_cairo(ctx)

        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = TestFrame(None, wx.ID_ANY, 'test rsvg', (200, 200), (800, 800))
    app.MainLoop()
    
    
