#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

#===============================================================================
# WebBrowser module.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import sys
import pygtk 
pygtk.require('2.0')
import gtk

if sys.platform=='win32':
    import win32con
    from ctypes import * 
    from ctypes.wintypes import *
    from comtypes import IUnknown
    from comtypes.automation import IDispatch, VARIANT
    from comtypes.client import wrap

    kernel32 = windll.kernel32
    user32 = windll.user32
    atl = windll.atl
else:
    import gtkmozembed
    
    
class Iexplore(gtk.DrawingArea):
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.expose_offset = False
        
        self.connect("expose_event", self.expose)


    def expose(self, widget=None, data=None):
        if self.expose_offset == True:
            return
        else:
            self.expose_offset = True
            
        # Make the container accept the focus and pass it to the control;
        # this makes the Tab key pass focus to IE correctly.
        self.set_property('can-focus', True)
        self.connect('focus', self.on_container_focus)

        # Resize the AtlAxWin window with its container.
        self.connect('size-allocate', self.on_container_size)

        # Create an instance of IE via AtlAxWin. 
        atl.AtlAxWinInit()
        hInstance = kernel32.GetModuleHandleA(None)
        parentHwnd = self.window.handle
        self.atlAxWinHwnd = user32.CreateWindowExA(0, 'AtlAxWin', 'about:',
            win32con.WS_VISIBLE | win32con.WS_CHILD | win32con.WS_HSCROLL |
            win32con.WS_VSCROLL, 0, 0, 100, 100, parentHwnd, None, hInstance, 0) 

        # Get the IWebBrowser2 interface for the IE control.
        pBrowserUnk = POINTER(IUnknown)()
        atl.AtlAxGetControl(self.atlAxWinHwnd, byref(pBrowserUnk))

        # the wrap call queries for the default interface
        self.browser = wrap(pBrowserUnk)

        # Create a Gtk window that refers to the native AtlAxWin window.
        self.gtkAtlAxWin = gtk.gdk.window_foreign_new(long(self.atlAxWinHwnd))


    def on_container_size(self, widget, sizeAlloc):
        self.gtkAtlAxWin.move_resize(0, 0, sizeAlloc.width, sizeAlloc.height)

    
    def on_container_focus(self, widget, data):
        # Used on win32 with Internet Explorer 
        # Pass the focus to IE. First get the HWND of the IE control; this
        # is a bit of a hack but I couldn't make IWebBrowser2._get_HWND work.

        rect = RECT()
        user32.GetWindowRect(self.atlAxWinHwnd, byref(rect))
        ieHwnd = user32.WindowFromPoint(POINT(rect.left, rect.top))
        user32.SetFocus(ieHwnd)
        
        
    # Basic browser functions -------------------------------------------------    
    def forward(self):
        try:
            self.browser.GoForward()
        except:
            pass
        
        
    def backward(self):
        try:
            self.browser.GoBack()
        except:
            pass
        
        
    def refresh(self):
        self.browser.Refresh()
        
        
    def stop(self):
        self.browser.Stop()
        
        
    def goto(self, url=''):
        v = byref(VARIANT())
        self.browser.Navigate(url, v, v, v, v)
        
        

class Mozilla:
    def __init__(self):
        self.browser = gtkmozembed.MozEmbed()
        
        
    # Basic browser functions -------------------------------------------------    
    def forward(self):
        if self.can_go_forward():
            self.go_forward()
            
        
    def backward(self):
        if self.can_go_back():
            self.go_back()
        
        
    def refresh(self):
        self.reload(gtkmozembed.FLAG_RELOADNORMAL)
        
        
    def stop(self):
        self.stop_load()
        
        
    def goto(self, url=''):
        self.load_url(url)
        
        
        
class Window:
    def __init__(self):
        self.home_url = 'http://www.majorsilence.com/'
        
        self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.win.set_title('Example Web browser that works on Linux and Windows')
        self.win.connect('destroy', gtk.main_quit)
        self.win.set_size_request(750, 550)
        #self.win.realize()
        self.win.show_all()
        
        self.main_vbox = gtk.VBox()

        control_box = gtk.HBox(False, 0)
        back = gtk.Button('Back')
        forward = gtk.Button('Forward')
        refresh = gtk.Button('Refresh')
        stop = gtk.Button('Stop')
        home = gtk.Button('Home')
        
        self.address = gtk.Entry(max=0) # no limit on address length
        
        # By default, clicking a GTK widget doesn't grab the focus away from 
        # a native Win32 control.
        self.address.connect('button-press-event', self.on_widget_click)
        
        go = gtk.Button('Go') 

        control_box.pack_start(back, True, True, 2)
        control_box.pack_start(forward, True, True, 2)
        control_box.pack_start(refresh, True, True, 2)
        control_box.pack_start(stop, True, True, 2)
        control_box.pack_start(home, True, True, 2)
        control_box.pack_start(self.address, True, True, 2)
        control_box.pack_start(go, True, True, 2)

        back.connect('clicked', self.on_backward_clicked, None)
        forward.connect('clicked', self.on_forward_clicked, None)
        refresh.connect('clicked', self.on_refresh_clicked, None) 
        stop.connect('clicked', self.on_stop_clicked, None) 
        home.connect('clicked', self.on_home_clicked, None)
        self.address.connect('key_press_event', self.on_address_keypress)
        go.connect('clicked', self.on_go_clicked, None)

        if sys.platform=='win32':
            self.BrowserPortlet = Iexplore()
        else: 
            self.BrowserPortlet = Mozilla()
            
        self.main_vbox.pack_start(control_box, False, True, 2) 
        self.win.add(self.main_vbox)            
        self.main_vbox.add(self.BrowserPortlet)         
        self.win.show_all()

                                        
    def on_widget_click(self, widget, data):
        # used on win32 platform because by default a gtk application does 
        # not grab control from native win32 control 
        self.win.window.focus()

        
    def on_backward_clicked(self, widget=None, data=None):
        self.BrowserPortlet.backward()


    def on_forward_clicked(self, widget=None, data=None):
        self.BrowserPortlet.forward()


    def on_refresh_clicked(self, widget=None, data=None):
        self.BrowserPortlet.refresh()
            

    def on_stop_clicked(self, widget=None, data=None):
        self.BrowserPortlet.stop()
            

    def on_home_clicked(self, widget=None, data=None):
        self.BrowserPortlet.goto(self.home_url)


    def on_go_clicked(self, widget=None, data=None):
        self.BrowserPortlet.goto(self.address.get_text())
            

    def on_address_keypress(self, widget, event):
        if gtk.gdk.keyval_name(event.keyval) == 'Return':
            print 'Key press: Return'
            self.on_go_clicked(None)
            
            

# Start the GTK mainloop ------------------------------------------------------
def main():
    gtk.main()
    return 0


if __name__ == "__main__":
    Window()
    main()
    
