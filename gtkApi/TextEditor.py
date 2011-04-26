#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

#===============================================================================
# TextEditor module.
# by Mark Muzenhardt, published under LGPL-License.
#===============================================================================

import pygtk
pygtk.require('2.0')
import gtk


class TextEditor:
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Translation Editor")
        window.connect("destroy", lambda w: gtk.main_quit())

        vbox = gtk.VBox()
        window.add(vbox)
        
        toolbar = gtk.Toolbar()
        vbox.pack_start(toolbar, expand=False, fill=True)
        
        button_print = gtk.Button('Druck')
        button_print.connect("clicked", self.on_button_print_clicked)
        toolbar.add(button_print)
        
        button_backward = gtk.Button('<-')
        toolbar.add(button_backward)
        button_forward = gtk.Button('->')
        toolbar.add(button_forward)
        
        button_cancel = gtk.Button('Abbruch')
        button_cancel.connect("clicked", lambda w: gtk.main_quit())
        toolbar.add(button_cancel)

        label = gtk.Label('NIIX')
        vbox.add(label)        
        window.show_all()
        
        
    # This methods are doing the initial --------------------------------------
    def on_button_print_clicked(self, widget=None, data=None):
        pass
        


# Start the GTK mainloop ------------------------------------------------------
def main():
    gtk.main()
    return 0


if __name__ == "__main__":
    TextEditor()
    main()
