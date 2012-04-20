# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wxApi.XRC
# by Mark Muzenhardt, published under LGPL license.
#===============================================================================

import wx, wx.xrc


class XrcBase(object):
    def __init__(self, parent, xrc_path, xrc_name):
        self.parent = parent
        self.xrc_path = xrc_path
        self.xrc_name = xrc_name
        self.xrc_resource = wx.xrc.XmlResource(self.xrc_path)


    def get_widget(self, widget_name):
        widget = wx.xrc.XRCCTRL(self, widget_name)
        return widget
        
        
        
class XrcDialog(XrcBase, wx.Dialog):
    def __init__(self, parent, xrc_path, xrc_name, size=wx.DefaultSize):
        self.pre_widget = wx.PreDialog()
        XrcBase.__init__(self, parent, xrc_path, xrc_name)
        
        self.xrc_resource.LoadOnDialog(self.pre_widget, self.parent, self.xrc_name)
        self.PostCreate(self.pre_widget)
        self.SetSize(size)
        
        
        
class XrcFrame(XrcBase, wx.Frame):
    def __init__(self, parent, xrc_path, xrc_name, size=wx.DefaultSize):
        self.pre_widget = wx.PreFrame()
        XrcBase.__init__(self, parent, xrc_path, xrc_name)
        
        self.xrc_resource.LoadOnFrame(self.pre_widget, self.parent, self.xrc_name)
        self.PostCreate(self.pre_widget)
        self.SetSize(size)
        


class XrcPanel(XrcBase, wx.Panel):
    def __init__(self, parent, xrc_path, xrc_name):
        self.pre_widget = wx.PrePanel()
        XrcBase.__init__(self, parent, xrc_path, xrc_name)
        
        self.xrc_resource.LoadOnPanel(self.pre_widget, self.parent, self.xrc_name)
        self.PostCreate(self.pre_widget)
        
        
        


