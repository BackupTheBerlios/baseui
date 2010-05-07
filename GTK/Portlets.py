# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.GTK Portlets module.
# by Mark Muzenhardt, published under BSD-License.
#
# Portlets are pre-defined widget-groups for common things to do, but without
# a window (or a container around it).
#===============================================================================

import gtk
import Entrys, Dialogs


class Login:
    ''' Dialog with 'Name' and 'Passwort' entrys to login. '''

    def __init__(self, comboboxentry_user=None,
                       entry_password=None):

        # Widget definitions --------------------------------------------------
        self.comboboxentry_user = Entrys.Combobox(comboboxentry_user)
        self.entry_password = Entrys.Simple(entry_password)
        return


    def create(self):
        self.comboboxentry_user = Entrys.Combobox().create()
        self.entry_password = Entrys.Simple().create()
        self.entry_password.set_visibility(False)
        
        table_definition = [
                               {'label': 'Benutzer', 'widget': self.comboboxentry_user.widget},
                               {'label': 'Passwort', 'widget': self.entry_password.widget}
                           ]
		
        # Table itself
        entry_table = Entrys.Table().create(table_definition)
        entry_table.set_border_width(border_width=8)

        self.widget = gtk.Frame(label='<b>Login</b>')
        label = self.widget.get_label_widget()
        label.set_use_markup(True)
        
        self.widget.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.widget.add(entry_table)
        return self.widget

    
    def populate(self, user_lod):
        ''' Populates the login entrys. The parameters has to be given as such:
                user_lod = [{'user': 'Mc Cready, Frank', 'password': 'Hellfire'}] 
            
            Note: There can be even more keys in the user_lod, for example a
                  primary key to identify the selection for sure. '''
                  
        print 'Function Dialogs.Login.populate currently not available,'
        print '    user_lod = ', user_lod,
        
        
    def get_permission(self):
        ''' Gives whether the entered password matches or not. '''
        
        user_dic = self.comboboxentry_user.get_selection()
        entered_password = self.entry_password.get_text()
        real_password = user_dic['password']
        
        if entered_password == real_password:
            return True
        else:
            return False
        
        
        
class Database:
    ''' Dialog to establish and connect databases '''

    def __init__(self, comboboxentry_engine=None,
                       comboboxentry_driver=None,
                       entry_database=None,
                       entry_host=None,
                       entry_user=None,
                       entry_password=None,
                       togglebutton_connection=None):

        # Predefinition -------------------------------------------------------
        self.database = None
        self.on_connect = None
        self.on_disconnect = None
        self.connect_order = None
        self.disconnect_order = None

        # Widget definitions --------------------------------------------------
        self.DialogBox = Dialogs.Simple(parent=None)
        self.comboboxentry_engine = Entrys.Combobox(comboboxentry_engine)
        self.entry_database = Entrys.Simple(entry_database)
        self.comboboxentry_driver = Entrys.Simple(comboboxentry_driver)
        self.entry_host = Entrys.Simple(entry_host)
        self.entry_user = Entrys.Simple(entry_user)
        self.entry_password = Entrys.Simple(entry_password)
        self.togglebutton_connection = togglebutton_connection

        # If exists, set widget image with disconnect.
        if self.togglebutton_connection <> None:
            self.set_disconnected()
            self.togglebutton_connection.connect('toggled', self.on_togglebutton_connection_toggled)

        if self.comboboxentry_engine.widget <> None:
            self.comboboxentry_engine.widget.connect('changed', self.on_comboboxentry_engine_changed)


    # Events ------------------------------------------------------------------
    def on_comboboxentry_engine_changed(self, widget=None, data=None):
        self.set_entrys_sensitivity(True)


    def on_togglebutton_connection_toggled(self, widget=None, data=None):
        if widget.get_active() == True:
            self.on_connect_event()
        else:
            self.on_disconnect_event()


    def on_connect_event(self):
        self.set_entrys_sensitivity(False)
        try:
            if self.connect_order <> None:
                self.connect_order()
        except:
            raise


    def on_disconnect_event(self):
        self.set_entrys_sensitivity(True)
        try:
            if self.disconnect_order <> None:
                self.disconnect_order()
        except:
            raise


    def set_entrys_sensitivity(self, onset=True):
        selection = self.comboboxentry_engine.get_selection()
        if selection <> None:
            selected_engine = True
        else:
            selected_engine = False

        if str(selection).lower() == 'odbc':
            self.comboboxentry_driver.widget.set_sensitive(selected_engine)   
        else:
            self.comboboxentry_driver.widget.set_sensitive(0)

        if str(selection).lower() == 'sqlite':
            self.entry_host.set_sensitive(0)
            self.entry_password.set_sensitive(0)
            self.entry_user.set_sensitive(0)
        else:
            self.entry_host.set_sensitive(onset)
            self.entry_password.set_sensitive(onset)
            self.entry_user.set_sensitive(onset)
            
        self.comboboxentry_engine.set_sensitive(onset)
        self.entry_database.set_sensitive(onset)
        if onset == False:
            self.comboboxentry_driver.set_sensitive(onset)
        
        
    # Actions -----------------------------------------------------------------
    def create(self):
        self.comboboxentry_engine = Entrys.Combobox().create()
        self.entry_database = Entrys.Simple().create()
        self.comboboxentry_driver = Entrys.Combobox().create()
        self.entry_host = Entrys.Simple().create()
        self.entry_user = Entrys.Simple().create()
        self.entry_password = Entrys.Simple().create()
        self.entry_password.set_visibility(False)

        table_definition = [
                               {'label': 'Engine', 'widget': self.comboboxentry_engine.widget},
                               {'label': 'Datenbank', 'widget': self.entry_database.widget},
                               {'label': 'ODBC-Treiber', 'widget': self.comboboxentry_driver.widget},
                               {'label': 'Host', 'widget': self.entry_host.widget},
                               {'label': 'Benutzer', 'widget': self.entry_user.widget},
                               {'label': 'Passwort', 'widget': self.entry_password.widget}
                           ]

        vbox = gtk.VBox()

        # Table itself
        self.entrys_table = Entrys.Table()
        table = self.entrys_table.create(table_definition)

        # Bottom buttons
        hbox = gtk.HBox()
        fixed_left = gtk.Fixed()
        fixed_right = gtk.Fixed()

        self.togglebutton_connection = gtk.ToggleButton()
        image_connect = gtk.Image()
        image_connect.set_from_stock(gtk.STOCK_DISCONNECT, gtk.ICON_SIZE_BUTTON)
        self.togglebutton_connection.add(image_connect)
        fixed_right.put(self.togglebutton_connection, x=0, y=0)

        hbox.pack_start(child=fixed_left, expand=True, fill=True, padding=0)
        hbox.pack_start(child=fixed_right, expand=False, fill=True, padding=0)

        vbox.pack_start(child=table, expand=True, fill=True, padding=0)
        vbox.pack_start(child=hbox , expand=False, fill=True, padding=0)
        vbox.set_border_width(border_width=8)

        self.widget = gtk.Frame(label='<b>Datenbank</b>')
        label = self.widget.get_label_widget()
        label.set_use_markup(True)
        
        self.widget.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.widget.add(vbox)
        
        # Callbacks
        self.comboboxentry_engine.widget.connect('changed', self.on_comboboxentry_engine_changed)
        self.togglebutton_connection.connect('toggled', self.on_togglebutton_connection_toggled)
        return self.widget


    def populate(self, db_engines_list=[], odbc_drivers_list=[], config_dic={}):
        ''' Fills the Database dialog with data from config_dic. '''
        
        # Set engines----------------------------------------------------------
        self.comboboxentry_engine.populate(db_engines_list)
        self.comboboxentry_driver.populate(odbc_drivers_list)
        
        if config_dic == None:
            return
        
        if config_dic.has_key('engine'):
            self.comboboxentry_engine.set_text(config_dic['engine'])
        if config_dic.has_key('database'):
            self.entry_database.widget.set_text(config_dic['database'])
        if config_dic.has_key('driver'):
            self.comboboxentry_driver.set_text(config_dic['driver'])
        if config_dic.has_key('host'):
            self.entry_host.widget.set_text(config_dic['host'])
        if config_dic.has_key('user'):
            self.entry_user.widget.set_text(config_dic['user'])
        if config_dic.has_key('password'):
            self.entry_password.widget.set_text(config_dic['password'])


    def get_config_dic(self):
        config_dic = {'engine': self.comboboxentry_engine.get_text(),
                      'database': self.entry_database.get_text(),
                      'driver': self.comboboxentry_driver.get_text(),
                      'host': self.entry_host.get_text(),
                      'user': self.entry_user.get_text(),
                      'password': self.entry_password.get_text()}
        return config_dic


    def set_connected(self):
        if self.on_connect <> None:
            self.on_connect()
        #self.connection_offset = True
        self.togglebutton_connection.set_active(1)
        #self.connection_offset = False
        image = self.togglebutton_connection.get_child()
        image.set_from_stock(gtk.STOCK_CONNECT, gtk.ICON_SIZE_BUTTON)


    def set_disconnected(self):
        if self.on_disconnect <> None:
            self.on_disconnect()
        #self.disconnecting = True
        self.togglebutton_connection.set_active(0)
        image = self.togglebutton_connection.get_child()
        image.set_from_stock(gtk.STOCK_DISCONNECT, gtk.ICON_SIZE_BUTTON)
        #self.disconnecting = False

        
        
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
        
        
        
class FTP:
    def __init__(self):
        # Predefinition -------------------------------------------------------
        self.on_connect = None
        self.on_disconnect = None
        self.connect_order = None
        self.disconnect_order = None
        
        
    def create(self):
        self.entry_hostname = Entrys.Simple().create()
        self.entry_username = Entrys.Simple().create()
        self.entry_password = Entrys.Simple().create()
        self.entry_password.set_visibility(False)
        
        table_definition = [
                               {'label': u'Rechnername',  'widget': self.entry_hostname.widget},
                               {'label': u'Benutzername', 'widget': self.entry_username.widget},
                               {'label': u'Kennwort',     'widget': self.entry_password.widget},
                           ]
                           
        vbox = gtk.VBox()

        # Table itself
        table = Entrys.Table().create(table_definition)

        # Bottom buttons
        hbox = gtk.HBox()
        fixed_left = gtk.Fixed()
        fixed_right = gtk.Fixed()

        self.togglebutton_connection = gtk.ToggleButton()
        image_connect = gtk.Image()
        image_connect.set_from_stock(gtk.STOCK_DISCONNECT, gtk.ICON_SIZE_BUTTON)
        self.togglebutton_connection.add(image_connect)
        fixed_right.put(self.togglebutton_connection, x=0, y=0)

        hbox.pack_start(child=fixed_left, expand=True, fill=True, padding=0)
        hbox.pack_start(child=fixed_right, expand=False, fill=True, padding=0)

        vbox.pack_start(child=table, expand=True, fill=True, padding=0)
        vbox.pack_start(child=hbox , expand=False, fill=True, padding=0)

        self.widget = gtk.Frame(label='<b>FTP-Zugang</b>')
        label = self.widget.get_label_widget()
        label.set_use_markup(True)
        
        self.widget.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.widget.add(vbox)

        # Callbacks
        self.togglebutton_connection.connect('toggled', self.on_togglebutton_connection_toggled)
        return self.widget
        
        
    # Events ------------------------------------------------------------------
    def on_togglebutton_connection_toggled(self, widget=None, data=None):
        if widget.get_active() == True:
            self.on_connect_event()
        else:
            self.on_disconnect_event()


    def on_connect_event(self):
        self.set_entrys_sensitivity(False)
        try:
            if self.connect_order <> None:
                self.connect_order()
        except:
            raise


    def on_disconnect_event(self):
        self.set_entrys_sensitivity(True)
        try:
            if self.disconnect_order <> None:
                self.disconnect_order()
        except:
            raise


    def set_entrys_sensitivity(self, onset=True):
        self.entry_hostname.set_sensitive(onset)
        self.entry_username.set_sensitive(onset)
        self.entry_password.set_sensitive(onset)
            
            
    def populate(self, config_dic={}):
        ''' Fills the FTP dialog with data from config_dic. '''
        
        if config_dic == None:
            return
        
        self.entry_hostname.set_text(config_dic.get('hostname', ''))
        self.entry_username.set_text(config_dic.get('username', ''))
        self.entry_password.set_text(config_dic.get('password', ''))
        
        
    def get_config_dic(self):
        config_dic = {'hostname': self.entry_hostname.get_text(),
                      'username': self.entry_username.get_text(),
                      'password': self.entry_password.get_text()}
        return config_dic
        
        
    def set_connected(self):
        if self.on_connect <> None:
            self.on_connect()
        #self.connection_offset = True
        self.togglebutton_connection.set_active(1)
        #self.connection_offset = False
        image = self.togglebutton_connection.get_child()
        image.set_from_stock(gtk.STOCK_CONNECT, gtk.ICON_SIZE_BUTTON)


    def set_disconnected(self):
        if self.on_disconnect <> None:
            self.on_disconnect()
        #self.disconnecting = True
        self.togglebutton_connection.set_active(0)
        image = self.togglebutton_connection.get_child()
        image.set_from_stock(gtk.STOCK_DISCONNECT, gtk.ICON_SIZE_BUTTON)
        #self.disconnecting = False
        
        
        
        