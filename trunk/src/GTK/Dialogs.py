# -*- coding: iso-8859-1 -*-

#===============================================================================
# GTKapi Dialogs module.
# by Mark Muzenhardt, published under BSD-License.
#
# Dialogs are pre-defined windows for common things to do.
#===============================================================================

import os, imp, traceback
import gtk

import Entrys
import Buttons

from Containers import Window
from Widgets import ProgressBar, TextView

PATH = os.path.dirname(__file__)


class Simple:
    def __init__(self, parent=None, encoding='latin-1'):
        ''' dialog_type is a string with following possible values:
                question = Ok/Cancel dialog.
                info     = Info dialog with one Ok-button.
                error    = Error dialog with one Ok-button.
            parent is the object of the parent window, needed if its modal or/and kept above. '''

        self.encoding = encoding
        
        if parent <> None:
            self.icon = parent.get_icon()
        else:
            self.icon = None

        self.set_parent(parent)


    def show(self, dialog_type='info', title='Info', text='', inst=None):
        if dialog_type == "question":
            dialog = gtk.Dialog(unicode(title, "latin-1"), None, flags=0, buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, \
                                                                                   gtk.STOCK_APPLY, gtk.RESPONSE_APPLY))
        elif dialog_type == "yesno":
            dialog = gtk.Dialog(unicode(title, "latin-1"), None, flags=0, buttons=(gtk.STOCK_YES, gtk.RESPONSE_YES, \
                                                                                   gtk.STOCK_NO, gtk.RESPONSE_NO))
        else:
            dialog = gtk.Dialog(unicode(title, "latin-1"), None, flags=0, buttons=(gtk.STOCK_OK, gtk.RESPONSE_OK))

        dialog.set_property("skip-taskbar-hint", True)
        dialog.set_property("skip-pager-hint", True)

        self.parent.remove_focus()
        dialog.set_keep_above(True)

        image = gtk.Image()
        image.set_padding(4, 4)
        if dialog_type == "error":
            image.set_from_stock(gtk.STOCK_DIALOG_ERROR, gtk.ICON_SIZE_DIALOG)
        elif dialog_type == "question" or dialog_type == "yesno":
            image.set_from_stock(gtk.STOCK_DIALOG_QUESTION, gtk.ICON_SIZE_DIALOG)
        elif dialog_type == "info":
            image.set_from_stock(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_DIALOG)

        if self.icon <> None:
            dialog.set_icon(self.icon)
        dialog.set_position("center")

        hbox = gtk.HBox()
        hbox.pack_start(image, expand=False, fill=True, padding=0)

        text = unicode(text, self.encoding) + "\n"
        
        if inst <> None:
            text += '<b>' + unicode(str(inst), 'latin-1') + '</b>\n\n'
            detail = '<span font_family = "monospace">' + traceback.format_exc() + '</span>'
            text += detail
                    
        label = gtk.Label(text)
        label.set_use_markup(True)
        label.set_line_wrap(1)
        label.set_padding(4, 4)
        vbox_text = gtk.VBox()
        vbox_text.pack_start(label, expand=True, fill=True, padding=0)
        hbox.pack_start(vbox_text, expand=True, fill=True, padding=0)

        dialog.vbox.pack_start(hbox, expand=True, fill=True, padding=0)
        
        # TODO: Do this with the instance Text of errors (with detail-button)
        #if inst <> None:
        #    textview_detail = TextView().create()
        #    textview_detail.populate(detail)
            #textview_detail.widget.set_padding(4, 4)
        #    vbox_text.pack_start(textview_detail.widget)
        dialog.show_all()

        response = dialog.run()
        self.parent.restore_focus()

        answer = None
        if response == gtk.RESPONSE_OK:
            answer = 'OK'
        if response == gtk.RESPONSE_APPLY:
            answer = 'APPLY'
        if response == gtk.RESPONSE_CANCEL:
            answer = 'CANCEL'
        if response == gtk.RESPONSE_YES:
            answer = 'YES'
        if response == gtk.RESPONSE_NO:
            answer = 'NO'
        dialog.destroy()
        return answer


    def set_parent(self, parent):
        self.parent = Window(parent)



class FileSelection:
    def __init__(self, parent=None):
        ''' parent = Parent window '''

        if parent <> None:
            self.icon = parent.get_icon()
        else:
            self.icon = None

        self.set_parent(parent)


    def show(self, dialog_type='open', title=''):
        ''' dialog_type = 'open' shows a file open dialog.
                          'save' shows a file save dialog.
                          'create folder' shows a folder creation dialog.
                          'select folder' shows a folder selection dialog.
            title = Fileselection dialog title as string. '''

        self.title = title

        if dialog_type == 'open':
            dialog_type = gtk.FILE_CHOOSER_ACTION_OPEN
        elif dialog_type == 'save':
            dialog_type = gtk.FILE_CHOOSER_ACTION_SAVE
        elif dialog_type == 'create folder':
            dialog_type = gtk.FILE_CHOOSER_ACTION_CREATE_FOLDER
        elif dialog_type == 'select folder':
            dialog_type = gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER

        file_selection_dialog = gtk.FileChooserDialog(unicode(self.title, "latin-1"),
                                                              None, dialog_type, ( \
                                                              gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                                              gtk.STOCK_OK, gtk.RESPONSE_OK))

        if self.icon <> None:
            file_selection_dialog.set_icon(self.icon)

        file_selection_dialog.set_default_response(gtk.RESPONSE_OK)
        self.parent.remove_focus()

        response = file_selection_dialog.run()
        self.parent.restore_focus()

        if response == gtk.RESPONSE_OK:
            filename = str(file_selection_dialog.get_filename())
            file_selection_dialog.destroy()
            return filename
        elif response == gtk.RESPONSE_CANCEL:
            file_selection_dialog.destroy()
            return None


    def set_parent(self, parent):
        self.parent = Window(parent)



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
        self.widget.set_border_width(border_width=8)
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
        self.DialogBox = Simple(parent=None)
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

        self.comboboxentry_engine.set_sensitive(onset)
        self.entry_database.set_sensitive(onset)
        if onset == False:
            self.comboboxentry_driver.set_sensitive(onset)
        self.entry_host.set_sensitive(onset)
        self.entry_password.set_sensitive(onset)
        self.entry_user.set_sensitive(onset)
        
        
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



class Start:
    ''' Dialog for application start up. '''

    def __init__(self):
        self.preferences_offset = False


    def on_button_preferences_clicked(self, widget=None, data=None):
        if widget.get_active():
            self.vbox.remove(self.image)
            self.vbox.pack_start(self.database_portlet)
            self.window.show_all()
        else:
            self.vbox.remove(self.database_portlet)
            self.vbox.pack_start(self.image)


    def on_button_cancel_clicked(self, widget=None, data=None):
        gtk.main_quit()


    def show(self, dialog_type='progress', start_image=None):
        ''' Shows the startup-dialog.
                dialog_type = 'progress'    shows dialog with progress bar.
                              'login'       shows dialog with name and password login.
                              'preferences' shows dialog with name and password login
                                            with 'Einstellungen' button to toggle the
                                            start image for a set of widgets. '''


        self.window = gtk.Window()
        self.window.set_position(gtk.WIN_POS_CENTER)

        self.vbox = gtk.VBox()
        self.window.add(self.vbox)

        self.image = gtk.Image()
        self.image.set_from_file(start_image)
        self.vbox.add(self.image)

        if dialog_type == 'database' or dialog_type == 'login':
            icon_pixbuf = self.window.render_icon(stock_id=gtk.STOCK_DIALOG_AUTHENTICATION, size=gtk.ICON_SIZE_SMALL_TOOLBAR, detail=None)
        else:
            icon_pixbuf = self.window.render_icon(stock_id=gtk.STOCK_EXECUTE, size=gtk.ICON_SIZE_SMALL_TOOLBAR, detail=None)
        self.window.set_icon(icon_pixbuf)

        if dialog_type == 'progress':
            self.window.set_decorated(False)

            self.progressbar = ProgressBar().create()
            self.vbox.add(self.progressbar.widget)
        elif dialog_type == 'login':
            self.window.set_title('Login')

            login_portlet = Login().create()

            self.button_cancel      = Buttons.Simple().create(label_text='_Abbruch', width=96)
            self.button_ok          = Buttons.Simple().create(label_text='_Ok', width=96)

            self.button_cancel.connect('clicked', self.on_button_cancel_clicked)

            left_button_list  = []
            right_button_list = [self.button_cancel,
                                 self.button_ok]

            bottom_portlet = BottomBox().create(left_button_list, right_button_list)

            self.vbox.pack_end(bottom_portlet, expand=False, fill=True)
            self.vbox.pack_end(login_portlet, expand=False, fill=True)
        elif dialog_type == 'database':
            self.window.set_title('Datenbank')

            print "Datenbank not yet implemented"
        elif dialog_type == 'database login':
            self.window.set_title('Datenbank Login')

            self.database_portlet = Database().create()
            self.database_portlet.set_border_width(border_width=8)
            
            login_portlet = Login().create()
            login_portlet.set_border_width(border_width=8)
            
            self.togglebutton_preferences = Buttons.Toggle().create(label_text='_Einstellungen', width=96)
            self.button_cancel      = Buttons.Simple().create(label_text='_Abbruch', width=96)
            self.button_ok          = Buttons.Simple().create(label_text='_Ok', width=96)

            self.togglebutton_preferences.connect('clicked', self.on_button_preferences_clicked)
            self.button_cancel.connect('clicked', self.on_button_cancel_clicked)

            left_button_list  = [self.togglebutton_preferences]
            right_button_list = [self.button_cancel,
                                 self.button_ok]

            bottom_portlet = BottomBox().create(left_button_list, right_button_list)

            self.vbox.pack_end(bottom_portlet, expand=False, fill=True)
            self.vbox.pack_end(login_portlet, expand=False, fill=True)
        self.window.show_all()


    def close(self):
        self.window.destroy()



class Serial:
	''' This is a simple serial-config dialog '''
	
	def __init__(self, parent=None):
		pass
		
		
		
	
class Progress:
    ''' This is a simple progress dialog. '''
    
    def __init__(self, parent=None):
        ''' parent = Parent window. '''

        if parent <> None:
            self.icon = parent.get_icon()
        else:
            self.icon = None

        self.parent = Window(parent)


    def on_window_destroy(self, widget=None, data=None):
        self.parent.restore_focus()


    def show(self, dialog_type='simple', title="Bitte warten...", text="Bitte warten..."):
        ''' dialog type is a string with following possible values:
            simple = Just a self destroying window with progress bar.
            cancel = A progress window with cancel-button. '''

        window = gtk.Window()
        # window.set_keep_above(True)
        window.set_property("skip-taskbar-hint", True)
        window.set_property("skip-pager-hint", True)
        window.connect("destroy", self.on_window_destroy)

        self.parent.remove_focus()

        image = gtk.Image()
        image.set_padding(4, 4)
        image.set_from_file(PATH + "/res/clock_32.png")

        if self.icon <> None:
            window.set_icon(self.icon)
        window.set_position("center")

        vbox = gtk.VBox()
        hbox = gtk.HBox()
        hbox.pack_start(image, True, True, 0)

        label = gtk.Label("\n" + unicode(text, "latin-1") + "\n")
        label.set_use_markup(True)
        label.set_line_wrap(1)
        label.set_padding(4, 4)
        hbox.pack_start(label, True, True, 0)
        vbox.pack_start(hbox, True, True, 0)

        self.progressbar = ProgressBar().create()
        vbox.pack_start(self.progressbar.widget, True, True, 0)
        window.add(vbox)
        window.show_all()


    def update(self, fraction=0):
        self.progressbar.update(fraction)



class BottomBox:
    def __init__(self):
        self.Button = Buttons.Simple(gtk.Button)
        self.button_dict = {}


    def create(self, left_button_list, right_button_list):
        ''' Creates buttons on the bottom of a window. The buttons can be left
            or right, depending on which button list contains the buttons.

            left_button_list = [gtk.Button('first'), gtk.Button('second')]
                               left aligned buttons,
            right_button_lit = [gtk.Button('fourth'), gtk.Button('third')]
                               right aligned buttons. '''


        # Bottom buttons
        self.widget = gtk.HBox()
        fixed_left = gtk.Fixed()
        fixed_right = gtk.Fixed()

        x_pos = 0
        for left_button in left_button_list:
            fixed_left.put(left_button, x=x_pos, y=0)
            x_pos, y_pos = left_button.size_request()
            x_pos += 4

        x_pos = 0
        for right_button in right_button_list:
            fixed_right.put(right_button, x=x_pos, y=0)
            x_pos, y_pos = right_button.size_request()
            x_pos += 4

        self.widget.pack_start(child=fixed_left, expand=True, fill=True, padding=0)
        self.widget.pack_start(child=fixed_right, expand=False, fill=True, padding=0)
        self.widget.set_border_width(border_width=8)
        return self.widget

