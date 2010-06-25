# -*- coding: iso-8859-1 -*-

#===============================================================================
# GTKapi Containers module.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import gtk, Widgets


class Base:
    def __init__(self, container, encoding='latin-1'):
        self.container = container
        self.encoding = encoding
        
    def connect(self, *args):
        self.container.connect(*args)
        
        
    def add(self, *args):
        self.container.add(*args)
        
        
    def show_all(self):
        self.container.show_all()
        
        
        
class Window(Base):
    def __init__(self, container=None, 
                       icon_file=None, 
                       stock_icon=None, 
                       title=None, 
                       trayify=False, 
                       gravity='center',
                       x_size=None, y_size=None,
                       encoding='latin-1'):
        
        Base.__init__(self, container, encoding)
        
        self.icon_file = icon_file
        self.stock_icon = stock_icon
        self.title = title
        self.focus_offset = False
        self.encoding = encoding
        self.gravity=gravity
        self.x_size=x_size
        self.y_size=y_size
        self.trayify = trayify
        
        self.TrayIcon = Widgets.TrayIcon()
        
        if self.container <> None:
            self.initialize()
        

    def on_window_state_event(self, window, event):
        # This checks if the window was minimized or unminimized
        if event.changed_mask & gtk.gdk.WINDOW_STATE_ICONIFIED:
            if event.new_window_state & gtk.gdk.WINDOW_STATE_ICONIFIED:
                # Window was minimized
                window.hide()
            else:
                # Window was unminimized!
                pass
    
    
    def on_tray_icon_activate(self):
        self.container.show()
        self.container.present()
    
    
    def create(self):
        self.container = gtk.Window()
        self.initialize()
        return self


    def show(self):
        self.container.show()


    def initialize(self):
        if self.icon_file <> None:
            pixbuf = gtk.gdk.pixbuf_new_from_file(self.icon_file)
            self.container.set_icon(pixbuf)

        if self.stock_icon <> None:
            pixbuf = self.window.render_icon(stock_id=self.stock_icon, size=gtk.ICON_SIZE_SMALL_TOOLBAR, detail=None)
            self.container.set_icon(pixbuf)

        if self.title <> None:
            self.container.set_title(unicode(self.title, self.encoding))
        
        if self.trayify == True:
            self.TrayIcon.create(self.icon_file, tooltip=self.title)
            self.TrayIcon.activate_function = self.on_tray_icon_activate
            self.container.connect('window-state-event', self.on_window_state_event)
            
        if self.x_size <> None and self.y_size <> None:
            self.container.set_size_request(self.x_size, self.y_size)
            
        if self.gravity == 'center':
            self.container.set_gravity(gtk.gdk.GRAVITY_CENTER)
            
            
    def remove_focus(self):
        if self.focus_offset == False:
            self.focus_offset = True
        else:
            return
        if self.container == None:
            return

        self.modal = self.container.get_modal()
        if self.modal:
            self.container.set_modal(False)
        return


    def restore_focus(self):
        if self.container == None:
            return

        self.set_modal(self.modal)
        self.focus_offset = False
        return
        
        
    def get_icon(self):
        return self.container.get_icon()    


    def destroy(self):
        self.container.destroy()
        
        
    def set_modal(self, modal):
        self.container.set_modal(modal)
        
        
    def get_modal(self):
        return self.container.get_modal()
        
        
    def set_gravity(self, gravity):
        self.container.set_gravity(gravity)
        
        
    def set_position(self, *args):
        self.container.set_position(*args)



class Tab:
    pass



class Frame:
    pass



