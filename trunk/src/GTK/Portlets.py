# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.GTK Portlets module.
# by Mark Muzenhardt, published under BSD-License.
#
# Portlets are pre-defined widget-groups for common things to do, but without
# a window (or a container around it).
#===============================================================================

import gtk
import Entrys


class Serial:
    def __init__(self, comboboxentry_port=None,
                       comboboxentry_baudrate=None,
                       comboboxentry_databits=None,
                       comboboxentry_parity=None,
                       comboboxentry_startbits=None,
                       comboboxentry_stopbits=None, encoding='latin-1'):
        
        pass
        #self.comboboxentry_port = Entrys.Combobox(comboboxentry_port)
        #self.comboboxentry_baudrate = Entrys.Combobox(comboboxentry_baudrate)
        #self.comboboxentry_databits = Entrys.Combobox(comboboxentry_databits)
        #self.comboboxentry_parity = Entrys.Combobox(comboboxentry_parity)
        #self.comboboxentry_stopbits = Entrys.Combobox(comboboxentry_stopbits)
        
        
    # Actions -----------------------------------------------------------------
    def create(self):
        self.comboboxentry_port = Entrys.Combobox().create()
        self.comboboxentry_baudrate = Entrys.Combobox().create()
        self.comboboxentry_driver = Entrys.Combobox().create()
        self.comboboxentry_databits = Entrys.Combobox().create()
        self.comboboxentry_parity = Entrys.Combobox().create()
        self.comboboxentry_stopbits = Entrys.Combobox().create()

        table_definition = [
                               {'label': u'Schnittstelle', 'widget': self.comboboxentry_port.widget},
                               {'label': u'Baud-Rate',     'widget': self.comboboxentry_baudrate.widget},
                               {'label': u'Datenbits',     'widget': self.comboboxentry_databits.widget},
                               {'label': u'Parität',       'widget': self.comboboxentry_parity.widget},
                               {'label': u'Stopbits',      'widget': self.comboboxentry_stopbits.widget}
                           ]

        vbox = gtk.VBox()

        # Table itself
        table = Entrys.Table().create(table_definition)

        # Bottom buttons
        hbox = gtk.HBox()
        fixed_left = gtk.Fixed()
        fixed_right = gtk.Fixed()

        #self.togglebutton_connection = gtk.ToggleButton()
        image_connect = gtk.Image()
        image_connect.set_from_stock(gtk.STOCK_DISCONNECT, gtk.ICON_SIZE_BUTTON)
        #self.togglebutton_connection.add(image_connect)
        #fixed_right.put(self.togglebutton_connection, x=0, y=0)

        hbox.pack_start(child=fixed_left, expand=True, fill=True, padding=0)
        hbox.pack_start(child=fixed_right, expand=False, fill=True, padding=0)

        vbox.pack_start(child=table, expand=True, fill=True, padding=0)
        vbox.pack_start(child=hbox , expand=False, fill=True, padding=0)
        vbox.set_border_width(border_width=8)

        self.widget = gtk.Frame(label='<b>Schnittstelle</b>')
        label = self.widget.get_label_widget()
        label.set_use_markup(True)
        
        self.widget.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.widget.add(vbox)
        self.widget.set_border_width(border_width=8)

        # Callbacks
        #self.comboboxentry_engine.widget.connect('changed', self.on_comboboxentry_engine_changed)
        #self.togglebutton_connection.connect('toggled', self.on_togglebutton_connection_toggled)
        return self
        
        
        
        