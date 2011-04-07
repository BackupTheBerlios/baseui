# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wxApi.Widgets
# by Mark Muzenhardt, published under LGPL license.
#===============================================================================

import wx

from Transformations import date_to_str


class TrayIcon(wx.TaskBarIcon):
    def __init__(self, frame, icon):
        wx.TaskBarIcon.__init__(self)
        
        self.frame = frame
        self.icon = icon
        
        # self.frame.Bind(wx.EVT_SIZE, self.on_size)
        self.frame.Bind(wx.EVT_ICONIZE, self.on_minimize)
        self.frame.Bind(wx.EVT_CLOSE, self.on_close)
        
        self.create_menu()
        self.Bind(wx.EVT_MENU, self.on_resume, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.on_resume, id=101)
        

    def create_menu(self):
        self.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.show_menu)
 
        self.menu = wx.Menu()
        self.menu.Append(101, u'&Wiederherstellen')
        self.menu.AppendSeparator()
        self.menu.Append(wx.ID_EXIT, u'&Schließen')
        

    def show_menu(self, event):
        self.PopupMenu(self.menu)

        
    def on_resume(self, event):
        self.RemoveIcon()
        self.frame.Show(True)
        self.frame.Iconize(False)

 
    def on_close(self, event):
        self.RemoveIcon()
        self.Destroy()
        event.Skip()
 
 
    def on_minimize(self, event):
        self.SetIcon(self.icon)
        self.frame.Show(False)
 
 
    # def on_size(self, event):   
    #     size = self.frame.GetClientSize()
    #     self.frame.text.SetSize(size)
    #     self.frame.panel.SetSize(size)
    #     event.Skip()
        
        

def widget_populator(widget_object, widget_content):
    #print 'pop:', widget_object, widget_content
    
    # FilePickerCtrl ---------------------------------------------------
    if widget_object.__class__ in [wx._controls.FilePickerCtrl, wx._controls.DirPickerCtrl]:
        if widget_content <> None:
            widget_object.SetPath(widget_content)
            
    # DatePickerCtrl ---------------------------------------------------
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
    
    # TextCtrl --------------------------------------------------------- 
    if widget_object.__class__ ==  wx._controls.TextCtrl:
        if widget_content <> None:
            if type(widget_content) <> unicode:
                widget_content = str(widget_content)
            widget_object.SetValue(widget_content.rstrip())
        else:
            widget_object.SetValue('')
    
    # Combobox ---------------------------------------------------------
    if widget_object.__class__ ==  wx._controls.ComboBox:
        # This works just if no foreign table is there, otherwise it will be overwritten!
        if widget_content <> None:
            if type(widget_content) <> unicode:
                widget_content = str(widget_content)
            widget_object.SetValue(widget_content.rstrip())
        else:
            widget_object.SetValue('')
            
    # Checkbox --------------------------------------------------------
    if widget_object.__class__ ==  wx._controls.CheckBox:
        if widget_content == '1' or \
           widget_content == 'Y' or \
           widget_content == True:
            widget_content = 1
        else:
            widget_content = 0
        widget_object.SetValue(int(widget_content))

    # Radiobutton ------------------------------------------------------
    if widget_object.__class__ == wx._controls.RadioButton:
        if widget_content == '1' or \
           widget_content == 'Y' or \
           widget_content == True:
            widget_content = 1
        else:
            widget_content = 0
        widget_object.SetValue(int(widget_content))
        
    # FilePickerCtrl ---------------------------------------------------
    if widget_object.__class__ == wx._controls.ColourPickerCtrl:
        if widget_content <> None:
            widget_object.SetColour(widget_content)

    
def widget_getter(widget_object):
    widget_content = None
    
    # Textctrl ---------------------------------------------------------
    if widget_object.__class__ ==  wx._controls.TextCtrl:
        widget_content = widget_object.GetValue()
        if widget_content == '':
            widget_content = None
    
    # Combobox ---------------------------------------------------------
    if widget_object.__class__ == wx._controls.ComboBox:
        # If this widget has a foreign relation, get client data. Else get Value.
        #if dic.get('referenced_column_name') <> None:
        # client_data = None
        selection = widget_object.GetSelection()
        widget_content = widget_object.GetValue()
        
        if selection <> -1:
            try:
                client_data = widget_object.GetClientData(selection)
                widget_content = client_data
            except Exception, inst:
                pass
        
        #else:
        #    widget_content = widget_object.GetValue()
        if widget_content == '':
            widget_content = None
    
    # Checkbox ---------------------------------------------------------
    if widget_object.__class__ == wx._controls.CheckBox:
        widget_content = widget_object.GetValue()
        
    # Radiobutton ------------------------------------------------------
    if widget_object.__class__ == wx._controls.RadioButton:
        widget_content = widget_object.GetValue()
        
    # Datepicker -------------------------------------------------------
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
    
    # Dir- and Filepicker ----------------------------------------------
    if widget_object.__class__ in [wx._controls.FilePickerCtrl, wx._controls.DirPickerCtrl]:
        widget_content = widget_object.GetTextCtrlValue()
        
    # Colourpicker -----------------------------------------------------
    if widget_object.__class__ == wx._controls.ColourPickerCtrl:
        colour = widget_object.GetColour()
        r, g, b = colour.Get()
        widget_content = '#%02x%02x%02x' % (r, g, b)
    return widget_content


