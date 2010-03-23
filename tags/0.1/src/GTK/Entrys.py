# -*- coding: iso-8859-1 -*-

#===============================================================================
# GTKapi Entrys module.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import gtk

from Transformations import *
from Widgets import *
from Containers import Window


class Base:
    def __init__(self, widget=None, encoding='latin-1'):
        self.widget = widget
        self.encoding = encoding
        
        
    def set_sensitive(self, onset=True):
        self.widget.set_sensitive(onset)
        
        
        
class Simple(Base):
    ''' Simple entry with validation abilities. '''

    def __init__(self, widget=None):
        Base.__init__(self, widget)
        
        self._wrapped = False
        self.data_type = str
        self.character_maximum_length = None
        self.numeric_precision = None
        self.numeric_scale = None
        self.is_nullable = True

        self.validity = True
        

    def on_expose(self, widget=None, data=None):
        if self._wrapped == False:
            self.wrap(widget)

        self.icon_area.draw_pixbuf(None, self.pixbuf, 0, 0, 0, 0, self.pixw, self.pixh)
        
    
    def wrap(self, widget):
        self._wrapped = True
        
        self.pixbuf = self.widget.render_icon(stock_id=gtk.STOCK_PRINT, size=gtk.ICON_SIZE_SMALL_TOOLBAR, detail=None)
        self.pixw = self.pixbuf.get_width()
        self.pixh = self.pixbuf.get_height()
        
        allocation = widget.get_allocation()
        entry_height = allocation.height
        entry_border = (entry_height-self.pixh)/2
        
        self.text_area = self.widget.window.get_children()[0]
        self.textx, self.texty = self.text_area.get_position()
        self.textw, self.texth = self.text_area.get_size()
        
        self.icon_area = gtk.gdk.Window(widget.window,
                             self.pixw, self.pixh,
                             gtk.gdk.WINDOW_CHILD,
                             (gtk.gdk.ENTER_NOTIFY_MASK |
                              gtk.gdk.LEAVE_NOTIFY_MASK),
                             gtk.gdk.INPUT_OUTPUT,
                             'icon window',
                             0, 0,
                             widget.get_visual(),
                             widget.get_colormap(),
                             gtk.gdk.Cursor(widget.get_display(), gtk.gdk.LEFT_PTR),
                             '', '', True)
        
        self.icon_area.move_resize(entry_border, entry_border, 
                                   self.pixw, self.pixh)
        self.text_area.move_resize(self.pixw + entry_border, self.texty, 
                                   self.textw-self.pixw-entry_border, self.texth)
        self.icon_area.show()
        
        
    def on_changed(self, widget=None, data=None):
        pass

                
    def set_text(self, text):
        self.widget.set_text(text)


    def get_text(self):
        return self.widget.get_text()


    def set_max_length(self, max_length):
        self.widget.set_max_length()
        
        
    def set_visibility(self, visibility):
        self.widget.set_visibility(visibility)
        

    def create(self):
        self.widget = gtk.Entry()
        return self


    def initialize(self, definition_dic=None, attributes_dic=None):
        ''' This function initializes database entrys for automatic validation
            and restriction. It is mainly used by the DataViews.Form class.

            definition_dic = Not now supported, but oneday it should look like that:
                             {'validation_function': self.validate,
                              'visible': True,
                              'editable': True,
                              'sensitive': True}

            attributes_dic = {'column_name': 'id',
                                  => Will be ignored like any other un-nesseccary crap-key.
                              'data_type': 'bigint',
                                  => Tells, if str, int or float content.
                              'character_maximum_length': = 20,
                                  => Restricts the maximum possible characters.
                              'numeric_precision' = 2,
                                  => Does nothing right now, but intended to validate floats in the future.
                              'numeric_scale' = ?,
                                  => Does nothing, too. Intended to validate number ranges in the future.
                              'is_nullable' = True}
                                  => Validates False if no content is given, which is the case for empty string.'''

        if self.widget == None:
            self.create()
        
        self.widget.connect('changed', self.on_changed)
        #self.widget.connect('expose-event', self.on_expose)
        
        self.definition_dic = definition_dic

        if attributes_dic <> None:
            self.definition_dic.update(attributes_dic)

        # Get type of awaited input for validation.
        if self.definition_dic.has_key('data_type'):
            self.data_type = SQL_to_DataType(self.definition_dic['data_type'])

        # Get maximum length for input restriction.
        if self.definition_dic.has_key('character_maximum_length'):
            self.character_maximum_length = self.definition_dic['character_maximum_length']
            self.widget.set_max_length(self.character_maximum_length)

        # Get numeric_precision for input validation.
        if self.definition_dic.has_key('numeric_precision'):
            self.numeric_precision = self.definition_dic['numeric_precision']

        # Get numeric_precision for input validation.
        if self.definition_dic.has_key('numeric_scale'):
            self.numeric_scale = self.definition_dic['numeric_scale']

        # Get nullable-flag for input validation.
        if self.definition_dic.has_key('is_nullable'):
            self.is_nullable = self.definition_dic['is_nullable']

        return


    def set_verification_function(self, verification_function=None):
        # TODO: Shut that crap off!
        self.verification_function = verification_function
        self.widget.connect('changed', on_changed)



class Table:
    def __init__(self):
        self.widget = None


    def create(self, table_definition):
        ''' Returns a table filled with labels and entrys.
            table_definition = [{label: 'Name', widget: gtk.Entry}] '''

        number_of_rows = len(table_definition)
        self.widget = gtk.Table(rows=number_of_rows, columns=2)

        for row_number in xrange(number_of_rows):
            content_dict = table_definition[row_number]

            label = gtk.Label(content_dict['label'])
            label.set_alignment(xalign=0, yalign=0.5)
            label.set_padding(4, 4)

            widget = content_dict['widget']
            widget.set_size_request(width=-1, height=24)

            self.widget.attach(label, left_attach=0, right_attach=1, top_attach=row_number, bottom_attach=row_number+1, xoptions=gtk.FILL, yoptions=gtk.FILL)
            self.widget.attach(widget, left_attach=1, right_attach=2, top_attach=row_number, bottom_attach=row_number+1, xoptions=gtk.EXPAND|gtk.FILL, yoptions=gtk.EXPAND)
        return self.widget



class Combobox(Base):
    def __init__(self, widget=None, encoding='latin-1'):
        Base.__init__(self, widget, encoding)

        self.definition_dic = None
        self.attributes_lod = None
        self.content_lod = None


    # Events ------------------------------------------------------------------
    def on_changed(self, widget=None, data=None):
        text = widget.get_text()
        combobox = widget.get_parent()
        model = combobox.get_model()

        row_number = 0
        for row in model:
            if text == row[1]:
                combobox.set_active(row_number)
                return
            row_number += 1
        return


    def create(self):
        self.widget = gtk.ComboBoxEntry()
        return self


    def initialize(self, definition_dic=None, attributes_lod=None):
        ''' This function initializes database entrys for automatic validation
            and restriction. It is mainly used by the DataViews.Form class.

            definition_dic = Defines the Entry attributes.
                             {'column_name': 'person.name',
                                  => column_name which contains the text for populating the combo-list.
                              'validation_function': self.validate,
                                  => if the attributes are not able to validate the input, this helps.
                              'visible': True,
                              'editable': True,
                              'sensitive': True,
                              'completion': True}

            attributes_lod = Defines the Table attributes.
                             [{'column_name': 'id',
                                  => Will be ignored like any other un-nesseccary crap-key.
                               'data_type': 'bigint',
                                  => Tells, if str, int or float content.
                               'character_maximum_length': = 20,
                                  => Restricts the maximum possible characters.
                               'numeric_precision' = 2,
                                  => Does nothing right now, but intended to validate floats in the future.
                               'numeric_scale' = ?,
                                  => Does nothing, too. Intended to validate number ranges in the future.
                               'is_nullable' = True}]
                                  => Validates False if no content is given, which is the case for empty string.'''

        self.definition_dic = definition_dic
        self.attributes_lod = attributes_lod


    def populate(self, content_lod=None):
        ''' Populates the ComboBox.
            content_lod = [{'id': 1, 'person.name': 'Foo'}] '''

        self.content_lod = content_lod
        liststore = gtk.ListStore(int, str)
        
        test_value = content_lod[0]
        if self.definition_dic <> None:
            column_name = self.definition_dic['column_name']
        for content_tuple in enumerate(self.content_lod):
            id = content_tuple[0]
            if type(test_value) == dict:
                if content_tuple[1][column_name] == None:
                    continue
                content = unicode(str(content_tuple[1][column_name]), self.encoding)
            else:
                if content_tuple[1] == None:
                    continue
                content = unicode(str(content_tuple[1]), self.encoding)
                
            liststore.append([id, content])

        model = self.widget.get_model()
        if model == None:
            self.widget.set_model(liststore)
            self.widget.set_text_column(1)
        else:
            self.widget.set_model(liststore)

        # Build completion
        completion = gtk.EntryCompletion()
        completion.set_model(liststore)
        completion.set_minimum_key_length(0)
        completion.set_text_column(1)
        completion.set_inline_completion(True)
        self.widget.child.set_completion(completion)

        self.widget.child.connect("changed", self.on_changed)
        return


    def get_selection(self):
        ''' Gives back the content_dic of the selected row. '''
        
        active = self.widget.get_active()
        model = self.widget.get_model()
        if active <> -1:
            id = model[active][0]
            selection = self.content_lod[id]
            return selection
        else:
            return


    def set_selection(self):
        ''' Sets the selection to '''
        

    def get_text(self):
        text = self.widget.child.get_text()
        return text
    
            
    def set_text(self, text):
        ''' Test text to given value. '''
        self.widget.child.set_text(text)
        


class Calendar:
    ''' Entry with date validation and togglebutton that pops up a calendar '''

    def __init__(self, togglebutton=None,
                       entry=None,
                       orientation='SW'):
        ''' togglebutton_calendar = Togglebutton to wrap into this class
            entry                 = Entry to wrap into this class
            orientation           = Orientation of Calendar widget around the togglebutton:
                                    SE = south east
                                    SW = south west
                                    NE = north east
                                    NW = north west '''

        self.entry = entry
        self.orientation = orientation.lower()
        self.parent = None

        # If no togglebutton given, search it!
        if togglebutton <> None:
            self.togglebutton = togglebutton
        else:
            table = self.entry.get_parent()
            list_of_children = table.get_children()

            for widget_object in list_of_children:
                widget_name = widget_object.get_name()
                if widget_name.startswith('fixed'):
                    fixed = widget_object
                    self.togglebutton = fixed.get_children()[0]

        self.togglebutton.connect('toggled', self.on_togglebutton_toggled)


    def on_togglebutton_toggled(self, widget=None, data = None):
        if widget.get_active() == 0:
            self.window.destroy()
        else:
            self.show(self.orientation, self.togglebutton, self.entry)


    def on_window_destroy(self, widget, data = None):
        self.togglebutton.set_active(0)
        self.parent.restore_focus()


    def on_calendar_day_selected(self, widget):
        """ Better take one-click-mode in that application """
        return


    def on_calendar_day_selected_double_click(self, widget):
        year, month, day = self.calendar.get_date()
        date_str = ""

        if len(str(day)) == 1:
            date_str = date_str + "0"
        date_str = date_str + str(day)+"."
        if len(str(month + 1)) == 1:
            date_str = date_str + "0"
        date_str = date_str + str(month+1)+"."+str(year)

        self.entry.set_text(date_str)
        self.window.destroy()


    def on_window_focus_out(self, widget, event):
        self.window.destroy()
        
        
    def create(self):
        return self


    def show(self, orientation, togglebutton, entry):
        """orientation = SE = south east
                         SW = south west
                         NE = north east
                         NW = north west
           togglebutton = bound gtk.ToggleButton
           entry = bound gtk.Entry"""

        self.entry = entry
        self.button_widget = togglebutton
        date = entry.get_text()

        if self.parent == None:
            self.parent = Window(get_window(self.entry))
        self.parent.remove_focus()

        self.window = gtk.Window()
        self.window.set_decorated(0)
        self.calendar = gtk.Calendar()
        self.window.add(self.calendar)
        self.window.show_all()
        
        self.window.connect('focus-out-event', self.on_window_focus_out)
        self.window.connect("destroy", self.on_window_destroy)
        self.calendar.connect("day-selected-double-click", self.on_calendar_day_selected_double_click)
        self.calendar.connect("day-selected", self.on_calendar_day_selected)

        togglebutton_allocation = togglebutton.get_allocation()
        togglebutton_x_pos = togglebutton_allocation.x
        togglebutton_y_pos = togglebutton_allocation.y
        togglebutton_width = togglebutton_allocation.width
        togglebutton_height = togglebutton_allocation.height

        window_x_pos, window_y_pos = togglebutton.window.get_origin()
        calendar_width, calendar_height = self.window.get_size()

        if orientation[0:1] == "n":
            calendar_y_pos = window_y_pos + togglebutton_y_pos - calendar_height
        else:
            calendar_y_pos = window_y_pos + togglebutton_y_pos + togglebutton_height

        if orientation[1:2] == "w":
            calendar_x_pos = window_x_pos + togglebutton_x_pos - calendar_width + togglebutton_width
        else:
            calendar_x_pos = window_x_pos + togglebutton_x_pos

        self.window.move(calendar_x_pos, calendar_y_pos)
        self.window.show()

        try:
            # This can be made better (with dateformat)
            self.day = int(date[0:2])
            self.month = int(date[3:5]) - 1
            self.year = int(date[6:10])
            self.calendar.select_month(self.month, self.year)
            self.calendar.select_day(self.day)
        except:
            pass

        self.entry = entry


    def set_text(self, text):
        self.entry.set_text(text)


    def get_text(self):
        return self.entry.get_text()



class IPaddress:
    pass



class URL:
    pass



class Currency:
    pass
