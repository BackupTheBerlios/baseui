"""

"""

import wx

def AddEllipticalArc(self, x, y, w, h, startAngle, endAngle, clockwise=False):
    """ Draws an arc of an ellipse within bounding rect (x,y,w,h) 
    from startArc to endArc (in radians, relative to the horizontal line of the eclipse)"""
    
    if True:
        import warnings
        warnings.warn("elliptical arcs are not supported")
        w = w/2.0
        h = h/2.0
        self.AddArc(x+w, y+h, ((w+h)/2), startAngle, endAngle, clockwise)
        return
    else:    
        #implement in terms of AddArc by applying a transformation matrix
        #Sigh this can't work, still need to patch wx to allow
        #either a) AddPath that's not a closed path or
        #b) allow pushing and popping of states on a path, not just on a context
        #a) is possible in GDI+, need to investigate other renderers.
        #b) is possible in Quartz and Cairo, but not in GDI+. It could
        #possibly be simulated by combining the current transform with option a.
        mtx = wx.GraphicsRenderer_GetDefaultRenderer().CreateMatrix()
        path = wx.GraphicsRenderer_GetDefaultRenderer().CreatePath()
            

        mtx.Translate(x+(w/2.0), y+(h/2.0))
        mtx.Scale(w/2.0, y/2.0)
        
        path.AddArc(0, 0, 1, startAngle, endAngle, clockwise)
        path.Transform(mtx)
        self.AddPath(path)
        self.MoveToPoint(path.GetCurrentPoint())
        self.CloseSubpath()
    
if not hasattr(wx.GraphicsPath, "AddEllipticalArc"):
    wx.GraphicsPath.AddEllipticalArc = AddEllipticalArc

del AddEllipticalArc
    