#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

#===============================================================================
# TranslationEditor module.
# by Mark Muzenhardt, published under LGPL-License.
#===============================================================================

import pygtk
pygtk.require('2.0')
import gtk
import Portlets

from gtkApi import Dialogs 
from gtkApi import DataViews


class TranslationEditor:
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
        
        self.DialogBox = Dialogs.Simple(parent=window)
        self.setup_table()
        
        vbox.add(self.table.widget)        
        window.show_all()
        
        
    # This methods are doing the initial --------------------------------------
    def on_button_print_clicked(self, widget=None, data=None):
        print 'Do print'


    def setup_table(self):
        definition_lod = \
        [
            {'column_name': 'name', 'column_label': 'Schlüsselwort', 'column_number': 0, 'data_type': 'varchar'},
            {'column_name': 'de',   'column_label': 'deutsch',       'column_number': 1, 'data_type': 'varchar'},
            {'column_name': 'en',   'column_label': 'englisch',      'column_number': 2, 'data_type': 'varchar'}
        ]

        content_lod = \
        [
            {'name': ''}
        ]

        try:
            self.table = DataViews.Tree(gtk.TreeView())
            self.table.initialize(definition_lod)
            self.table.populate(content_lod)
        except Exception, inst:
            self.DialogBox.show(dialog_type="error", title="Fehler", inst=inst)
            

# Start the GTK mainloop ------------------------------------------------------
def main():
    gtk.main()
    return 0


if __name__ == "__main__":
    TranslationEditor()
    main()
