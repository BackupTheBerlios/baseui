# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wxApi.Widgets
# by Mark Muzenhardt, published under LGPL license.
#===============================================================================

import wx


class TrayIcon(wx.TaskBarIcon):
    def __init__(self, frame, icon):
        wx.TaskBarIcon.__init__(self)
        
        self.frame = frame
        self.icon = icon
        
        # self.frame.Bind(wx.EVT_SIZE, self.on_size)
        self.frame.Bind(wx.EVT_ICONIZE, self.on_minimize)
        self.frame.Bind(wx.EVT_CLOSE, self.on_close)
        
        self.create_menu()
        self.Bind(wx.EVT_MENU, self.on_resume, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.on_resume, id=101)
        

    def create_menu(self):
        self.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.show_menu)
 
        self.menu = wx.Menu()
        self.menu.Append(101, u'&Wiederherstellen')
        self.menu.AppendSeparator()
        self.menu.Append(wx.ID_EXIT, u'&Schließen')
        

    def show_menu(self, event):
        self.PopupMenu(self.menu)

        
    def on_resume(self, event):
        self.RemoveIcon()
        self.frame.Show(True)
        self.frame.Iconize(False)

 
    def on_close(self, event):
        self.RemoveIcon()
        self.Destroy()
        event.Skip()
 
 
    def on_minimize(self, event):
        self.SetIcon(self.icon)
        self.frame.Show(False)
 
 
    # def on_size(self, event):   
    #     size = self.frame.GetClientSize()
    #     self.frame.text.SetSize(size)
    #     self.frame.panel.SetSize(size)
    #     event.Skip()
        
        
