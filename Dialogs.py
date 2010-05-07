# -*- coding: iso-8859-1 -*-

#===============================================================================
# Dialog module.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import gtk
import Portlets

from GTK import Buttons
from GTK.Dialogs import BottomBox


class StartDialog:
    def __init__(self):
        #self.database_portlet = DatabaseLogin()
        #self.user_portlet = UserLogin()
        self.window = gtk.Window()
        self.window.set_position(gtk.WIN_POS_CENTER)
        
        icon_pixbuf = self.window.render_icon(stock_id=gtk.STOCK_DIALOG_AUTHENTICATION, size=gtk.ICON_SIZE_SMALL_TOOLBAR, detail=None)
        self.window.set_icon(icon_pixbuf)
        
        self.database = None
       # self.start_image = start_image
        
        
    def on_button_preferences_clicked(self, widget=None, data=None):
        if widget.get_active():
            self.vbox.remove(self.image)
            self.vbox.pack_start(self.database_portlet)
            self.window.show_all()
        else:
            self.vbox.remove(self.database_portlet)
            self.vbox.pack_start(self.image)


    def on_button_ok_clicked(self, widget=None, data=None):
        #self.database_dialog.save_settings_to_ini()
        pass
        
        
    def on_button_cancel_clicked(self, widget=None, data=None):
        gtk.main_quit()
        
    
    def on_connect(self):
        self.database = self.database_dialog.database
        print 'connected!'
        
        
    def on_disconnect(self):
        print 'disconnected.'
        
    
    def show(self, start_image, ini_filename):
        self.vbox = gtk.VBox()
        self.window.add(self.vbox)

        self.image = gtk.Image()
        self.image.set_from_file(start_image)
        self.vbox.add(self.image)

        # This makes the user login
        self.login_dialog = Portlets.UserLogin(parent=self.window)
        self.login_portlet = self.login_dialog.portlet

        # Connects the database and populates the database_portlet.
        self.database_dialog = Portlets.DatabaseLogin(ini_filename, parent=self.window, autosave=True)
        self.database_portlet = self.database_dialog.portlet
        self.database_dialog.set_connect_function(self.on_connect)
        #self.database_dialog.set_disconnect_function(self.on_disconnect)
        
        print 'database:', self.database
        
        self.togglebutton_preferences = Buttons.Toggle().create(label_text='_Einstellungen', width=96)
        self.button_cancel      = Buttons.Simple().create(label_text='_Abbruch', width=96)
        self.button_ok          = Buttons.Simple().create(label_text='_Ok', width=96)

        self.togglebutton_preferences.connect('clicked', self.on_button_preferences_clicked)
        self.button_ok.connect('clicked', self.on_button_ok_clicked)
        self.button_cancel.connect('clicked', self.on_button_cancel_clicked)

        left_button_list  = [self.togglebutton_preferences]
        right_button_list = [self.button_cancel,
                             self.button_ok]

        bottom_portlet = BottomBox().create(left_button_list, right_button_list)

        self.vbox.pack_end(bottom_portlet, expand=False, fill=True)
        self.vbox.pack_end(self.login_portlet, expand=False, fill=True)
        self.window.show_all()
        
        self.database_dialog.connect()
        
    
    def close(self):
        self.window.destroy()
        
        