# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wxApi.Widgets
# by Mark Muzenhardt, published under LGPL license.
#===============================================================================

import wx, string

from Transformations import date_to_str


# This has been set up to optionally use the wx.BufferedDC if
# USE_BUFFERED_DC is True, it will be used. Otherwise, it uses the raw
# wx.Memory DC , etc.

USE_BUFFERED_DC = 1

class BufferedWindow(wx.Window):

    """

    A Buffered window class.

    To use it, subclass it and define a Draw(DC) method that takes a DC
    to draw to. In that method, put the code needed to draw the picture
    you want. The window will automatically be double buffered, and the
    screen will be automatically updated when a Paint event is received.

    When the drawing needs to change, you app needs to call the
    UpdateDrawing() method. Since the drawing is stored in a bitmap, you
    can also save the drawing to file by calling the
    SaveToFile(self,file_name,file_type) method.

    """


    def __init__(self, parent, id,
                 pos = wx.DefaultPosition,
                 size = wx.DefaultSize,
                 style = wx.NO_FULL_REPAINT_ON_RESIZE):
        wx.Window.__init__(self, parent, id, pos, size, style)

        wx.EVT_PAINT(self, self.OnPaint)
        wx.EVT_SIZE(self, self.OnSize)

        # OnSize called to make sure the buffer is initialized.
        # This might result in OnSize getting called twice on some
        # platforms at initialization, but little harm done.
        self.OnSize(None)

    def Draw(self,dc):
        ## just here as a place holder.
        ## This method should be over-ridden when subclassed
        pass

        
    def OnPaint(self, event):
        # All that is needed here is to draw the buffer to screen
        if USE_BUFFERED_DC:
            dc = wx.BufferedPaintDC(self, self._Buffer)
        else:
            dc = wx.PaintDC(self)
            dc.DrawBitmap(self._Buffer,0,0)

            
    def OnSize(self,event):
        # The Buffer init is done here, to make sure the buffer is always
        # the same size as the Window
        Size  = self.GetClientSizeTuple()
        #print Size

        # Make new offscreen bitmap: this bitmap will always have the
        # current drawing in it, so it can be used to save the image to
        # a file, or whatever.
        self._Buffer = wx.EmptyBitmap(*Size)
        self.UpdateDrawing()

        
    def SaveToFile(self,FileName,FileType):
        ## This will save the contents of the buffer
        ## to the specified file. See the wxWindows docs for 
        ## wx.Bitmap::SaveFile for the details
        self._Buffer.SaveFile(FileName,FileType)

        
    def UpdateDrawing(self):
        """
        This would get called if the drawing needed to change, for whatever reason.

        The idea here is that the drawing is based on some data generated
        elsewhere in the system. If that data changes, the drawing needs to
        be updated.

        """

        if USE_BUFFERED_DC:
            dc = wx.BufferedDC(wx.ClientDC(self), self._Buffer)
            self.Draw(dc)
        else:
            # update the buffer
            dc = wx.MemoryDC()
            dc.SelectObject(self._Buffer)
            self.Draw(dc)
            # update the screen
            wx.ClientDC(self).DrawBitmap(self._Buffer,0,0)

            

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
        
        
def widget_initializator(definition_dict):
    widget_object = definition_dict.get('widget_object')
    data_type = definition_dict.get('data_type')
    character_maximum_length = definition_dict.get('character_maximum_length')
    
    if widget_object.__class__ in [wx._controls.TextCtrl]:
        if character_maximum_length <> None:
            widget_object.SetMaxLength(character_maximum_length)

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
            if chr(key) in string.digits:
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

        # Returning without calling even.Skip eats the event before it
        # gets to the text control
        return



def widget_populator(widget_object, widget_content, data_type=None):
    #print 'pop:', widget_object, widget_content, data_type
    
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

    
def widget_getter(widget_object, data_type=None):
    widget_content = None
    
    # Textctrl ---------------------------------------------------------
    if widget_object.__class__ ==  wx._controls.TextCtrl:
        widget_content = widget_object.GetValue()
        if data_type == 'money':
            widget_content = widget_content.replace(',', '.')
            #print '...', widget_object, widget_content
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
                #print '...', widget_object, data_type, type(widget_content), widget_content
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
            #print 'content:', widget_content, 'in widget', widget_object, 'of data_type:', data_type, 'not able to convert to', convert
    return widget_content


