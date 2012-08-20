# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wxApi.Widgets
# by Mark Muzenhardt, published under BSD license.
#===============================================================================

import wx, string, wx.combo
import datetime

from Transformations import date_to_str
from pprint import pprint


class BufferedWindow(wx.ScrolledWindow):
    def __init__(self, parent, id,
                 pos = wx.DefaultPosition,
                 size = wx.DefaultSize,
                 style = wx.NO_FULL_REPAINT_ON_RESIZE):
        wx.ScrolledWindow.__init__(self, parent, id, pos, size, style)

        wx.EVT_PAINT(self, self.OnPaint)
        wx.EVT_SIZE(self, self.OnSize)
        wx.EVT_SCROLLWIN(self, self.OnScroll)
        self.OnSize(None)
    
    
    def Draw(self, dc):
        pass

        
    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self, self._Buffer)
        
    
    def OnScroll(self, event):
        Size  = self.GetClientSizeTuple()
        self._Buffer = wx.EmptyBitmap(*Size)
        self.UpdateDrawing()
        event.Skip()
        
                
    def OnSize(self, event):
        Size  = self.GetClientSizeTuple()
        self._Buffer = wx.EmptyBitmap(*Size)
        self.UpdateDrawing()

        
    def SaveToFile(self, FileName, FileType):
        self._Buffer.SaveFile(FileName, FileType)
        
        
    def UpdateDrawing(self):
        dc = wx.BufferedDC(wx.ClientDC(self), self._Buffer)
        self.DoPrepareDC(dc)
        dc.Clear()
        self.Draw(dc)
        
        

class FontStyleCombobox(wx.combo.OwnerDrawnComboBox):
    def __init__(self, parent):
        self._font_list = self.get_font_list()
        wx.combo.OwnerDrawnComboBox.__init__(self, parent, choices=self._font_list, size=(180, 26))
        
        
    def OnDrawItem(self, dc, rect, item, flags):
        if item == wx.NOT_FOUND:
            # painting the control, but there is no valid item selected yet
            return
            
        r = wx.Rect(*rect)  # make a copy
        r.Deflate(3, 14)
        
        face = self._font_list[item]
        
        if flags & wx.combo.ODCB_PAINTING_CONTROL:
            # for painting the control itself
            #dc.DrawLine( r.x+5, r.y+r.height/2, r.x+r.width - 5, r.y+r.height/2 )
            pass
        else:
            font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, face)
            dc.SetFont(font)
            # for painting the items in the popup
            dc.DrawText(self.GetString(item),
                        r.x + 3,
                        (r.y + 0) + ( (r.height/2) - dc.GetCharHeight() )/2)
            
           
    # Overridden from OwnerDrawnComboBox, called for drawing the
    # background area of each item.
    def OnDrawBackground(self, dc, rect, item, flags):
        # If the item is selected, or its item # iseven, or we are painting the
        # combo control itself, then use the default rendering.
        if (item & 1 == 0 or flags & (wx.combo.ODCB_PAINTING_CONTROL |
                                      wx.combo.ODCB_PAINTING_SELECTED)):
            wx.combo.OwnerDrawnComboBox.OnDrawBackground(self, dc, rect, item, flags)
            return

        # Otherwise, draw every other background with different colour.
        bgCol = wx.Colour(240,240,250)
        dc.SetBrush(wx.Brush(bgCol))
        dc.SetPen(wx.Pen(bgCol))
        dc.DrawRectangleRect(rect);


    def get_font_list(self):
        e = wx.FontEnumerator()
        e.EnumerateFacenames()
        font_list = e.GetFacenames()
        font_list.sort()
        #print font_list
        return font_list
        
    # Overridden from OwnerDrawnComboBox, should return the height
    # needed to display an item in the popup, or -1 for default
    def OnMeasureItem(self, item):
        # Simply demonstrate the ability to have variable-height items
    #    if item & 1:
    #        return 36
    #    else:
            return 32

    # Overridden from OwnerDrawnComboBox.  Callback for item width, or
    # -1 for default/undetermined
    #def OnMeasureItemWidth(self, item):
    #    return -1; # default - will be measured from text width
    
    
    
class TrayIcon(wx.TaskBarIcon):
    def __init__(self, frame, icon, tooltip=''):
        wx.TaskBarIcon.__init__(self)
        
        self.frame = frame
        self.icon = icon
        self.tooltip = tooltip
        
        self._mintotray = True
        self._evertray = False
        
        self.Bind(wx.EVT_TASKBAR_LEFT_UP, self.on_left_up)
        self.frame.Bind(wx.EVT_ICONIZE, self.on_minimize)
        
        
    def on_left_up(self, event):
        if self.frame.IsIconized():
            self.frame.Iconize(False)
            self.frame.Show()
            self.frame.Restore()
            self.RemoveIcon()
            
        
    def on_minimize(self, event):
        if event.Iconized():
            self.frame.Hide()
            self.frame.Iconize(True)
            self.SetIcon(self.icon, self.tooltip)
            
        
        
def init_widgets(definition_dict):
    widget_object = definition_dict.get('widget_object')
    data_type = definition_dict.get('data_type')
    character_maximum_length = definition_dict.get('character_maximum_length')
    referenced_table_object = definition_dict.get('referenced_table_object')
    
    # Handle the textctrl
    if widget_object.__class__ in [wx._controls.TextCtrl]:
        if character_maximum_length <> None:
            widget_object.SetMaxLength(character_maximum_length)
            
        widget_object.SetValidator(ValidateDataType(data_type))
        
    # Handle the combobox
    if widget_object.__class__ in [wx._controls.ComboBox]:
        # On a foreign key column validation makes no sense!
        if referenced_table_object == None:
            widget_object.SetValidator(ValidateDataType(data_type))



class ValidateDataType(wx.PyValidator):
    def __init__(self, data_type):
        wx.PyValidator.__init__(self)
        
        self.data_type = data_type
        
        self.Bind(wx.EVT_CHAR, self.OnChar)
        
    
    def Clone(self):
        return ValidateDataType(self.data_type)
    
    
    def OnChar(self, event):
        key = event.GetKeyCode()

        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return
        
        if self.data_type in ['integer', 'bigint']:
            if chr(key) in '-' + string.digits:
                event.Skip()
                return
        elif self.data_type in ['float', 'money']:
            if chr(key) in ',.' + string.digits:
                event.Skip()
                return
        else:
            event.Skip()
            return
        
        if not wx.Validator_IsSilent():
            wx.Bell()
            
        # Returning without calling event.Skip eats the event before it
        # gets to the text control
        return



def populate_widget(widget_object, widget_content, data_type=None):
    ''' This function checks, which widget the widget_object is. Then, it populates
        the given widget with the widget_content by converting it to a fitting
        type. If data_type is given, it also formats the widget_content depending
        on the data_type. 
        
        This function is especially used for populating the widgets of a form
        with database content or other external data.'''
        
    # FilePickerCtrl -----------------------------------------------------------
    if widget_object.__class__ in [wx._controls.FilePickerCtrl, wx._controls.DirPickerCtrl]:
        if widget_content <> None:
            widget_object.SetPath(widget_content)
            
    # DatePickerCtrl -----------------------------------------------------------
    if widget_object.__class__ ==  wx._controls.DatePickerCtrl:
        if widget_content <> None:
            widget_content = date_to_str(widget_content)
            dt = widget_content.split('.')
            day = int(dt[0])
            month = int(dt[1])-1
            year = int(dt[2])
            
            datetime = wx.DateTime()
            datetime.Set(day=day, month=month, year=year)
            widget_object.SetValue(datetime)
    
    # TextCtrl -----------------------------------------------------------------
    if widget_object.__class__ ==  wx._controls.TextCtrl:
        if data_type == 'money':
            widget_object.SetWindowStyleFlag(widget_object.GetWindowStyleFlag() | wx.TE_RIGHT)
            if widget_content <> None:
                widget_content = '%.2f' % float(widget_content)
                widget_content = widget_content.replace('.', ',')

        if widget_content <> None:
            if type(widget_content) <> unicode:
                widget_content = str(widget_content)
            widget_object.SetValue(widget_content.rstrip())
        else:
            widget_object.SetValue('')
    
    # Combobox -----------------------------------------------------------------
    if widget_object.__class__ ==  wx._controls.ComboBox:
        # This works just if no foreign table is there, otherwise it will be overwritten!
        if widget_content <> None:
            if type(widget_content) <> unicode:
                widget_content = str(widget_content)
            widget_object.SetValue(widget_content.rstrip())
        else:
            widget_object.SetValue('')
            
    # Checkbox -----------------------------------------------------------------
    if widget_object.__class__ ==  wx._controls.CheckBox:
        if widget_content == '1' or \
           widget_content == 'Y' or \
           widget_content == True:
            widget_content = 1
        else:
            widget_content = 0
        widget_object.SetValue(int(widget_content))

    # Radiobutton --------------------------------------------------------------
    if widget_object.__class__ == wx._controls.RadioButton:
        if widget_content == '1' or \
           widget_content == 'Y' or \
           widget_content == True:
            widget_content = 1
        else:
            widget_content = 0
        widget_object.SetValue(int(widget_content))
        
    # Choice -------------------------------------------------------------------
    if widget_object.__class__ == wx._controls.Choice:
        if widget_content <> None:
            widget_object.SetStringSelection(widget_content)
        
    # ColourPickerCtrl -----------------------------------------------------------
    if widget_object.__class__ == wx._controls.ColourPickerCtrl:
        if widget_content <> None:
            widget_object.SetColour(widget_content)

    
def get_widget_value(widget_object, data_type=None):
    widget_content = None
    
    # Textctrl -----------------------------------------------------------------
    if widget_object.__class__ ==  wx._controls.TextCtrl:
        widget_content = widget_object.GetValue()
        if data_type == 'money':
            widget_content = widget_content.replace(',', '.')
        elif data_type == 'datetime':
            try:
                dt=datetime.datetime.strptime(widget_content, '%Y-%m-%d %H:%M:%S')
            except:
                dt=None
            widget_content = dt

        if widget_content == '':
            widget_content = None

    
    # Combobox -----------------------------------------------------------------
    if widget_object.__class__ == wx._controls.ComboBox:
        # If this widget has a foreign relation, get client data, else get Value.
        # if dic.get('referenced_column_name') <> None:
        # client_data = None
        selection = widget_object.GetSelection()
        widget_content = widget_object.GetValue()
        
        if selection <> -1:
            try:
                client_data = widget_object.GetClientData(selection)
                widget_content = client_data
            except Exception, inst:
                pass

        if widget_content == '':
            widget_content = None
    
    # Checkbox -----------------------------------------------------------------
    if widget_object.__class__ == wx._controls.CheckBox:
        widget_content = widget_object.GetValue()
        
    # Radiobutton --------------------------------------------------------------
    if widget_object.__class__ == wx._controls.RadioButton:
        widget_content = widget_object.GetValue()
    
    # Choice -------------------------------------------------------------------
    if widget_object.__class__ == wx._controls.Choice:
        widget_content = widget_object.GetStringSelection()
            
    # Datepicker ---------------------------------------------------------------
    if widget_object.__class__ == wx._controls.DatePickerCtrl:
        widget_content = widget_object.GetValue()
        
        if widget_content.IsValid() == False:
            widget_content = None
            return widget_content
            
        # Not pretty, but works for MSsql over odbc.
        year = widget_content.GetYear()
        month = widget_content.GetMonth() + 1
        day = widget_content.GetDay()
        widget_content = '%02i.%02i.%04i' % (day, month, year)
    
    # Dir- and FilePicker ------------------------------------------------------
    if widget_object.__class__ in [wx._controls.FilePickerCtrl, wx._controls.DirPickerCtrl]:
        widget_content = widget_object.GetTextCtrlValue()
        
    # ColourPicker -------------------------------------------------------------
    if widget_object.__class__ == wx._controls.ColourPickerCtrl:
        colour = widget_object.GetColour()
        r, g, b = colour.Get()
        widget_content = '#%02x%02x%02x' % (r, g, b)
    
    convert = None
    if data_type == 'bigint':
        convert = long
    if data_type == 'integer':
        convert = int
    if data_type in ['float', 'money']:
        convert = float
    
    if convert <> None:
        try:
            widget_content = convert(widget_content)
        except:
            pass
    return widget_content


def convert_length(entry, choice):
    ''' This funtion converts the value of the entry into the unit of the 
        choice. The ChoiceStringSelection can be m (meter) or ft (feet). '''
    
    value = entry.GetValue()
    unit = choice.GetStringSelection()
    feet = 0.3048
    
    if value <> '':
        value = int(value)
    
    if unit == 'm':
        value = round(value * feet, 0)
    elif unit == 'ft':
        value = round(value / feet, 0)
    entry.SetValue(str(int(value)))
    

        
class RedirectText(object):
    def __init__(self, entry):
        self.out = entry
        
        
    def write(self, string):
        self.out.SetStyle(self.out.GetLastPosition(), self.out.GetLastPosition(), wx.TextAttr(wx.BLACK, wx.WHITE))
        self.out.WriteText(string)
        self.out.ShowPosition(self.out.GetLastPosition())
        
        

class RedirectError:
    """ Class to redirect stderr text """    
    def __init__(self, entry):
        self.out=entry
        
        
    def write(self, string):
        self.out.SetStyle(self.out.GetLastPosition(), self.out.GetLastPosition(), wx.TextAttr(wx.RED, wx.WHITE))
        self.out.WriteText(string)
        self.out.ShowPosition(self.out.GetLastPosition())
        
        
        
class wrap_time_slider(object):
    def __init__(self, slider, entry, choice):
        self.slider = slider
        self.slider.Bind(wx.EVT_SLIDER, self.on_slider)
        
        self.entry = entry
        self.entry.SetWindowStyle(wx.TE_PROCESS_ENTER)
        self.entry.Bind(wx.EVT_TEXT_ENTER, self.on_entry_enter)
        self.entry.Bind(wx.EVT_KILL_FOCUS, self.on_entry_kill_focus)
        
        # This wraps the SetValue method of the entry to override it with set_time.
        self.set_entry_value = self.entry.SetValue
        self.entry.SetValue = self.set_time
        self.entry.GetValue = self.get_time
        
        self.choice = choice
        self.choice.Bind(wx.EVT_CHOICE, self.on_choice)
        
        self._change_function_list = []
        self._units = [{'unit': 'ms',  'factor': 1,       'max': 1000},
                       {'unit': 's',   'factor': 1000,    'max':   60},
                       {'unit': 'min', 'factor': 60000,   'max':   60},
                       {'unit': 'h',   'factor': 3600000, 'max':   24}]
        self.init_choice()
        self.init_slider()
        
        self._time = 1000
        self.set_time(self._time)
        
        
    def on_slider(self, event=None):
        value = self.slider.GetValue()
        self.set_time(self.calc_time(value * self._slider_factor), False)
        
        
    def init_slider(self):
        unit, factor, max = self.get_selected_unit()
        self._slider_factor = 1
        if max > 100:
            self._slider_factor = max / 100
        
        
    def on_entry_enter(self, event=None):
        value = int(self.entry.GetValue())
        self.set_time(self.calc_time(value), True)
        
    
    def on_entry_kill_focus(self, event):
        self.set_time(self._time, False)
        event.Skip()
        
        
    def get_time(self):
        return self._time
    
    
    def set_time(self, time, correct_unit=True):
        ''' Set the widget to a time in ms. '''
        
        # Time could come as string from SetValue on the entry widget.
        time = int(time)
        
        # Set the best unit if correct_unit is True
        unit, factor, max = self.get_selected_unit()
        if correct_unit == True:
            unit, factor, max = self.set_time_unit(time)
        
        value = time / factor
        self.set_entry_value(str(value))
        
        self.slider.SetRange(1, max / self._slider_factor)
        self.slider.SetValue(value / self._slider_factor)
        self._time = time
        
        for function in self._change_function_list:
            function()
        
        
    def on_choice(self, event=None):
        unit, factor, max = self.get_selected_unit()
        value = int(self.entry.GetValue())
        self.init_slider()
        self.set_time(self._time, False)
        
        
    def init_choice(self):
        self.choice.Clear()
        for unit_dict in self._units:
            self.choice.Append(unit_dict['unit'], unit_dict)
        self.choice.SetSelection(0)
        
        
    def set_time_unit(self, time):
        unit, factor, max = self.get_selected_unit()
        if time > max * factor or time < factor:
            for unit_dict in self._units:
                unit, factor, max = self.unpack_unit_dict(unit_dict)
                
                if time <= factor * max:
                    break
                
        self.choice.SetStringSelection(unit)
        self.init_slider()
        return unit, factor, max
        
        
    def get_selected_unit(self):
        selection = self.choice.GetSelection()
        unit_dict = self.choice.GetClientData(selection)
        return self.unpack_unit_dict(unit_dict)
        
        
    def calc_time(self, value):
        unit, factor, max = self.get_selected_unit()
        return value * factor
    
    
    def unpack_unit_dict(self, unit_dict):
        return unit_dict['unit'], unit_dict['factor'], unit_dict['max']
        

    def add_change_function(self, function):
        self._change_function_list.append(function)
        
        
        
class wrap_log_entry(object):
    def __init__(self, entry):
        self.entry = entry
        
        
    def write(self, string):
        self.entry.SetStyle(self.out.GetLastPosition(), self.out.GetLastPosition(), wx.TextAttr(wx.BLACK, wx.WHITE))
        self.entry.ShowPosition(self.out.GetLastPosition())
        self.entry.WriteText(string)
        
        
        
        