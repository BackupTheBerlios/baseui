# -*- coding: iso-8859-1 -*-#
#!/usr/bin/env python2.4

import wx
import calendar, datetime, time

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
        print Size

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

            
            
class GanttChart(BufferedWindow):
    def __init__(self, parent, id = -1):
        ## Any data the Draw() function needs must be initialized before
        ## calling BufferedWindow.__init__, as it will call the Draw
        ## function.
        
        self.scale = 1.0
        self.year = 2011
        self.month = 1
        
        self.DrawData = {}
        BufferedWindow.__init__(self, parent, id)

    def Draw(self, dc):        
        dc.SetBackground( wx.Brush("White") )
        dc.Clear() # make sure you clear the bitmap!
        print 'zoom: %i' % int(self.scale*100)
        top_left_corner =     ( 10 * self.scale,  10 * self.scale)
        bottom_right_corner = (630 * self.scale, 470 * self.scale)
        
        day_size =  ( 20 * self.scale, 20 * self.scale)
        name_size = (100 * self.scale, 25 * self.scale)
        
        monthnames_row = 0
        calendarweeks_row = 1
        weekdaynumbers_row = 2
        weekdaynames_row = 3
        graph_row = 4
        
        content_lod = [
        {'name': u'Herbert Ärbert',  'id': 0},
        {'name': u'Kalinka Kefir',   'id': 1},
        {'name': u'Ritchie Ritch',   'id': 2},
        {'name': u'Özculücé, Erkan', 'id': 3},
        {'name': u'Mark Muzenhardt', 'id': 4}]
        
        weekend_color = '#FFAA00'
        foreground_color = 'black'
        background_color = 'white'
        
        # private values ------------------------------------------------------
        weekdays = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
        monthnames = ['Januar', 'Februar', u'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
        
        first_weekday = calendar.monthrange(self.year, self.month)[0]
        number_of_monthdays = calendar.monthrange(self.year, self.month)[1]
        
        monthnames_offset = (name_size[0], monthnames_row * day_size[1])
        calendarweeks_offset = (name_size[0], calendarweeks_row * day_size[1])
        weekdaynumbers_offset = (name_size[0], weekdaynumbers_row * day_size[1])
        weekdaynames_offset = (name_size[0], weekdaynames_row * day_size[1])
        graph_offset = (0, graph_row * day_size[1])
        
        # draw top top ruler --------------------------------------------------
        dc.SetPen(wx.Pen(foreground_color, 1))
        
        font_size = day_size[0] / 2
        font = wx.Font(pointSize=font_size,
                       family=wx.FONTFAMILY_DEFAULT,
                       style=wx.FONTSTYLE_NORMAL, 
        #               face='Lucida Console', 
                       weight=wx.FONTWEIGHT_NORMAL)
        dc.SetFont(font)
        
        cal_week_start_xpos = None
        for day in xrange(1, number_of_monthdays+1):
            date = datetime.date(self.year, self.month, day)
            time_tuple = date.timetuple()
            weekday = time_tuple.tm_wday
            weekday_str = weekdays[weekday]
            calendar_week = date.isocalendar()[1]
            
            ruler_x_pos = top_left_corner[0] + ((day-1) * day_size[0])
            dc.SetBrush(wx.Brush('white'))
            
            if cal_week_start_xpos == None:
                cal_week_start_xpos = ruler_x_pos
            
            # Draw year
            pass
            
            # Draw monthname
            if day == number_of_monthdays:
                dc.DrawRectangle(x=top_left_corner[0] + monthnames_offset[0], 
                                 y=top_left_corner[1] + monthnames_offset[1], 
                                 width=(day_size[0] * number_of_monthdays) + 1, 
                                 height=day_size[1] + 1)
                                 
                text_offset = self.center_text(dc, weekday_str, day_size)
                dc.DrawText(text='%s' % monthnames[self.month-1],
                            x=top_left_corner[0] + text_offset[0] + monthnames_offset[0], 
                            y=top_left_corner[1] + text_offset[1] + monthnames_offset[1])
                            
            # Draw calendar-week
            if weekday == 0:
                cal_week_start_xpos = ruler_x_pos 
            if weekday == 6 or day == number_of_monthdays:
                dc.DrawRectangle(x=cal_week_start_xpos + calendarweeks_offset[0], 
                                 y=top_left_corner[1] + calendarweeks_offset[1], 
                                 width=(day_size[0] * (weekday+1))+1, 
                                 height=day_size[1] + 1)
                                 
                text_offset = self.center_text(dc, weekday_str, day_size)
                dc.DrawText(text='KW %i' % calendar_week,
                            x=cal_week_start_xpos + text_offset[0] + calendarweeks_offset[0], 
                            y=top_left_corner[1] + text_offset[1] + calendarweeks_offset[1])
                
            if weekday >= 5:
                dc.SetBrush(wx.Brush(weekend_color))
            else:
                dc.SetBrush(wx.Brush(background_color))
                
            # Draw day by number
            dc.DrawRectangle(x=ruler_x_pos + weekdaynumbers_offset[0], 
                             y=top_left_corner[1] + weekdaynumbers_offset[1], 
                             width=day_size[0]+1, 
                             height=day_size[1] + 1)
                             
            text_offset = self.center_text(dc, str(day), day_size)
            dc.DrawText(text=str(day), 
                        x=ruler_x_pos + text_offset[0] + weekdaynumbers_offset[0],
                        y=top_left_corner[1] + text_offset[1] + weekdaynumbers_offset[1])
            
            # Draw day by weekday
            dc.DrawRectangle(x=ruler_x_pos + weekdaynames_offset[0], 
                             y=top_left_corner[1] + weekdaynames_offset[1], 
                             width=day_size[0]+1, 
                             height=day_size[1] + 1)
                             
            
            text_offset = self.center_text(dc, weekday_str, day_size)
            dc.DrawText(text=weekday_str, 
                        x=ruler_x_pos + text_offset[0] + weekdaynames_offset[0], 
                        y=top_left_corner[1] + text_offset[1] + weekdaynames_offset[1])
                        
        # Draw dudes
        row = 0
        for content in content_lod:
            dc.DrawRectangle(x=top_left_corner[0] + graph_offset[0], 
                             y=top_left_corner[1] + graph_offset[1] + (row*name_size[1]), 
                             width=name_size[0] + 1, 
                             height=name_size[1] + 1)
                             
            text_offset = self.center_text(dc, content.get('name'), name_size)
            dc.DrawText(text=content.get('name'), 
                        x=top_left_corner[0] + text_offset[0], 
                        y=top_left_corner[1] + text_offset[1] + graph_offset[1] + (row*name_size[1]))
            
            for day in xrange(1, number_of_monthdays+1):
                ruler_x_pos = top_left_corner[0] + ((day-1) * day_size[0])
                
                date = datetime.date(self.year, self.month, day)
                time_tuple = date.timetuple()
                weekday = time_tuple.tm_wday
                
                if weekday >= 5:
                    dc.SetBrush(wx.Brush(weekend_color))
                else:
                    dc.SetBrush(wx.Brush(background_color))
                    
                dc.DrawRectangle(x=ruler_x_pos + weekdaynumbers_offset[0], 
                                 y=top_left_corner[1] + graph_offset[1] + (row*name_size[1]), 
                                 width=day_size[0] + 1, 
                                 height=name_size[1] + 1)
                             
            row += 1
            
                    
    def center_text(self, dc, text='', size=(0,0)):
        text_size = dc.GetTextExtent(text)
        text_offset = ((size[0] - text_size[0]) / 2, ((size[1]-text_size[1]) / 2))
        return text_offset        
        

class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Double Buffered Test",
                         wx.DefaultPosition,
                         size=(500,500),
                         style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)

        ## Set up the MenuBar
        MenuBar = wx.MenuBar()

        file_menu = wx.Menu()
        ID_EXIT_MENU = wx.NewId()
        file_menu.Append(ID_EXIT_MENU, "E&xit","Terminate the program")
        wx.EVT_MENU(self, ID_EXIT_MENU, self.OnQuit)
        MenuBar.Append(file_menu, "&File")

        draw_menu = wx.Menu()
        ID_DRAW_MENU = wx.NewId()
        draw_menu.Append(ID_DRAW_MENU, "&New Drawing","Update the Drawing Data")
        wx.EVT_MENU(self, ID_DRAW_MENU,self.NewDrawing)
        BMP_ID = wx.NewId()
        draw_menu.Append(BMP_ID,'&Save Drawing\tAlt-I','')
        wx.EVT_MENU(self,BMP_ID, self.SaveToFile)
        MenuBar.Append(draw_menu, "&Draw")

        self.SetMenuBar(MenuBar)
        
        self.Bind(wx.EVT_MOUSEWHEEL, self.on_mousewheel)
        
        self.Window = GanttChart(self)

    def OnQuit(self,event):
        self.Close(True)

    def on_mousewheel(self, event):
        print event.GetWheelRotation(),
        
        if event.GetWheelRotation() > 0:
            self.Window.scale += (self.Window.scale / 10)
            if self.Window.scale*100 > 1000:
                self.Window.scale = 10.0
        else:
            self.Window.scale -= (self.Window.scale / 10)
            if self.Window.scale*100 < 10:
                self.Window.scale = 0.1
        self.Window.UpdateDrawing()
        
        
    def NewDrawing(self,event):
        self.Window.UpdateDrawing()
        
        
    def SaveToFile(self,event):
        dlg = wx.FileDialog(self, "Choose a file name to save the image as a PNG to",
                           defaultDir = "",
                           defaultFile = "",
                           wildcard = "*.png",
                           style = wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            self.Window.SaveToFile(dlg.GetPath(),wx.BITMAP_TYPE_PNG)
        dlg.Destroy()

    

class DemoApp(wx.App):
    def OnInit(self):
        #wx.InitAllImageHandlers() # called so a PNG can be saved      
        frame = TestFrame()
        frame.Show(True)

        ## initialize a drawing
        ## It doesn't seem like this should be here, but the Frame does
        ## not get sized until Show() is called, so it doesn't work if
        ## it is put in the __init__ method.
        frame.NewDrawing(None)

        self.SetTopWindow(frame)

        return True

if __name__ == "__main__":
    print "about to initialize the app"
    app = DemoApp(0)
    app.MainLoop()
