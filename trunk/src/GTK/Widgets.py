# -*- coding: iso-8859-1 -*-

#===============================================================================
# GTKapi Widgets module.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import os
import gtk, gobject

PATH = os.path.dirname(__file__)


class TextView:
    def __init__(self, widget=None, font=None, encoding='latin-1'):
        self.widget = widget
        self.text_buffer = self.widget.get_buffer()
        self.font = font
        self.encoding = encoding
            

    def create(self):
        self.widget = gtk.TextView()
        return self


    def write(self, *args):
        number_of_args = len(args)
        for iter in xrange(number_of_args):
            text = args[iter]
            if iter < (number_of_args - 1):
                text += ' '
            self.text_buffer.insert_at_cursor(unicode(text, self.encoding))
        if self.font <> None:
            self.set_font(self.font)
            

    def populate(self, text):
        self.text_buffer.set_text(unicode(text, self.encoding))
        if self.font <> None:
            self.set_font(self.font)
    
    
    def get_text(self):
        start_iter = self.text_buffer.get_start_iter()
        end_iter = self.text_buffer.get_end_iter()
        text = self.text_buffer.get_text(start_iter, end_iter)
        return text
    
    
    def set_font(self, font):
        tag_table = self.text_buffer.get_tag_table()
        first_tag = gtk.TextTag(name=None)
        first_tag.set_property("font", font)
        tag_table.add(first_tag)
            
        start_iter = self.text_buffer.get_start_iter()
        end_iter = self.text_buffer.get_end_iter()
        self.text_buffer.apply_tag(first_tag, start_iter, end_iter)
        
        
    def set_text(self, text):
        ''' Should be inserted soon! '''
        self.text_buffer.insert_at_cursor(text)
        pass
        


class TrayIcon:
    def __init__(self, widget=None):
        self.widget = widget
        self.filename = ''
        self.tooltip = ''
        
        self.activate_function = None
        self.popup_menu_function = None
        

    def on_status_icon_activate(self, widget=None, data=None):
        self.activate_function()


    def on_status_icon_popup_menu(self, widget=None, button=None, activate_time=None, data=None):
        print 'popup menu:', widget, button, activate_time, data


    def show(self):
        pass


    def hide(self):
        pass


    def create(self, filename=None, tooltip=None):
        self.tooltip = tooltip
        self.filename = filename

        self.widget = gtk.StatusIcon()
        
        if self.filename <> None:
            self.widget.set_from_file(self.filename)
        if self.tooltip <> None:
            self.widget.set_tooltip(self.tooltip)

        self.widget.connect('popup-menu', self.on_status_icon_popup_menu)
        self.widget.connect('activate', self.on_status_icon_activate)
        return self
        
    
    #def set_activate_function(self, activate_function):
    #    self.activate_function = activate_function



class ProgressBar:
    def __init__(self, widget=None):
        self.widget = widget


    def create(self):
        self.widget = gtk.ProgressBar()
        return self


    def update(self, fraction=0):
        self.widget.set_fraction(fraction)
        self.widget.set_text(str(int(fraction * 100)) + " %")

        while gtk.events_pending():
            gtk.main_iteration()


            
def get_window(widget):
    parent = widget.get_parent()
    while parent <> None:
        last_parent = parent
        parent = parent.get_parent()
    return last_parent
