# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wxApi.Calendars module.
# by Mark Muzenhardt, published under LGPL license.
#===============================================================================

import wx
import calendar, datetime, time

from Widgets import BufferedWindow


weekend_color = '#FFAA00'
foreground_color = 'black'
background_color = 'white'

weekdays = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
monthnames = ['Januar', 'Februar', u'M�rz', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']

        
        
class DayChart(BufferedWindow):
    def __init__(self, parent):
        pass
        
        self.parent = parent
        self.start_date = None
        self.end_date = None
        
        self.line_width = 1.0
        #self.scale = 1.0
        #self.year = 2011
        #self.month = 7
        #self.start_day = 4
        #self.end_day = 8
        
#        content = [
#            {'name': u' 6:00'},
#            {'name': u' 7:00'},
#            {'name': u' 8:00'},
#            {'name': u' 9:00'},
#            {'name': u'10:00'},
#            {'name': u'11:00'},
#            {'name': u'12:00'},
#            {'name': u'13:00'},
#            {'name': u'14:00'},
#            {'name': u'15:00'},
#            {'name': u'16:00'},
#            {'name': u'17:00'},
#            {'name': u'18:00'},
#            {'name': u'19:00'},
#            {'name': u'20:00'},
#        ]
#        
#        self.content = content
        
        BufferedWindow.__init__(self, parent, id=wx.ID_ANY)
        self.SetSize(parent.GetSize())
        self.parent.Bind(wx.EVT_SIZE, self.on_resize)
        
        self.Bind(wx.EVT_MOUSEWHEEL, self.on_mousewheel)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_mouse_right_down)
        
        
    def on_resize(self, event):
        self.SetSize(self.parent.GetSize())
        
        
    def on_mousewheel(self, event):
        #print event.GetWheelRotation() #, event.GetWheelDelta()
        pass
    
    
    def on_mouse_right_down(self, event):
        #print 'right button down'
        pass
        
        
    def set_date_range(self, start_date=None, end_date=None, nof_days=None):
        ''' start_date and end_date are date objects, which are giving the
            date range to the calendar. Optionally, nof_days can be given instead
            of end_date or start_date (so that only two of three values must be 
            given). '''
        
        if start_date == None:
            delta = datetime.timedelta(days=nof_days)
            self.start_date = end_date - delta
        else:
            self.start_date = start_date
        
        if nof_days == None:
            delta = end_date - start_date
            self.nof_days = delta.days
        else:
            self.nof_days = nof_days
            
        if end_date == None:
            delta = datetime.timedelta(days=nof_days)
            self.end_date = start_date + delta
        else:
            self.end_date = end_date
        
        self.UpdateDrawing()
        # print 'start_date:', self.start_date, 'end_date', self.end_date, 'days:', self.nof_days
    
        
    def Draw(self, dc):
        dc.SetBackground(wx.Brush("White"))
        dc.Clear()
        
        if self.start_date == None or self.end_date == None:
            return
        
        # Set the corners of the drawing
        parent_size = self.parent.GetSize()
        top_left_corner =     ( 10,  10)
        bottom_right_corner = (parent_size[0] - 10, parent_size[1] - 10)
        
        # Set the field sizes for the content.
        clocktime_size = (100, 50)
        day_size =  (100, 50)
        
        line_width = self.line_width
        
        monthnames_row = 0
        weekdaynumbers_row = 1
        weekdaynames_row = 2
        graph_row = 3
        
        monthnames_offset = (clocktime_size[0], monthnames_row * day_size[1])
        weekdaynumbers_offset = (clocktime_size[0], weekdaynumbers_row * day_size[1])
        weekdaynames_offset = (clocktime_size[0], weekdaynames_row * day_size[1])
        graph_offset = (0, graph_row * day_size[1])
        
        # draw top top ruler --------------------------------------------------
        dc.SetPen(wx.Pen(foreground_color, line_width))
        
        if day_size[0] > day_size[1]:
            smaller_size = day_size[1]
        font_size = (smaller_size / 2) * 0.6
        font = wx.Font(pointSize=font_size,
                       family=wx.FONTFAMILY_DEFAULT,
                       style=wx.FONTSTYLE_NORMAL, 
                       #face='Lucida Console', 
                       weight=wx.FONTWEIGHT_NORMAL)
        dc.SetFont(font)
        
        end_delta = self.end_date - self.start_date
        cal_week_start_xpos = None
        for day_delta in xrange(0, end_delta.days + 1):
            day_date = self.start_date + datetime.timedelta(days=day_delta)
            day = day_date.day
            week = day_date.isocalendar()[1]
            month = day_date.month
            year = day_date.year
            weekday_str = self.get_weekday(date=day_date, string=True)
            
            ruler_x_pos = top_left_corner[0] + ((day_delta-1) * day_size[0])
            dc.SetBrush(wx.Brush('white'))
            
            if cal_week_start_xpos == None:
                cal_week_start_xpos = ruler_x_pos
            
            # Draw year
            pass
            
            # Draw day by number
            dc.DrawRectangle(x=ruler_x_pos + weekdaynumbers_offset[0], 
                             y=top_left_corner[1] + weekdaynumbers_offset[1], 
                             width=day_size[0] + line_width, 
                             height=day_size[1] + line_width)
                             
            text_offset = self.center_text(dc, str(day), day_size)
            dc.DrawText(text=str(day), 
                        x=ruler_x_pos + text_offset[0] + weekdaynumbers_offset[0],
                        y=top_left_corner[1] + text_offset[1] + weekdaynumbers_offset[1])
                
            # Draw day by weekday
            dc.DrawRectangle(x=ruler_x_pos + weekdaynames_offset[0], 
                             y=top_left_corner[1] + weekdaynames_offset[1], 
                             width=day_size[0] + line_width, 
                             height=day_size[1] + line_width)
                                              
            text_offset = self.center_text(dc, weekday_str, day_size)
            dc.DrawText(text=weekday_str, 
                        x=ruler_x_pos + text_offset[0] + weekdaynames_offset[0], 
                        y=top_left_corner[1] + text_offset[1] + weekdaynames_offset[1])
                        
            #continue
            
            # Draw monthname
#            if day == number_of_monthdays:
#                dc.DrawRectangle(x=top_left_corner[0] + monthnames_offset[0], 
#                                 y=top_left_corner[1] + monthnames_offset[1], 
#                                 width=(day_size[0] * number_of_monthdays) + line_width, 
#                                 height=day_size[1] + line_width)
#                                 
#                text_offset = self.center_text(dc, weekday_str, day_size)
#                dc.DrawText(text='%s %s (KW %s)' % (monthnames[self.month-1], str(self.year), str(calendar_week)),
#                            x=top_left_corner[0] + text_offset[0] + monthnames_offset[0], 
#                            y=top_left_corner[1] + text_offset[1] + monthnames_offset[1])
#
#            
        # Draw dudes
        # row = 0
#        for content in self.content:
#            dc.DrawRectangle(x=top_left_corner[0] + graph_offset[0], 
#                             y=top_left_corner[1] + graph_offset[1] + (row*name_size[1]), 
#                             width=name_size[0] + line_width, 
#                             height=name_size[1] + line_width)
#                             
#            text_offset = self.center_text(dc, content.get('name'), name_size)
#            dc.DrawText(text=content.get('name'), 
#                        x=top_left_corner[0] + text_offset[0], 
#                        y=top_left_corner[1] + text_offset[1] + graph_offset[1] + (row*name_size[1]))
#            
#            for day in xrange(1, number_of_monthdays+1):
#                ruler_x_pos = top_left_corner[0] + ((day-1) * day_size[0])
#                
#                date = datetime.date(self.year, self.month, day)
#                time_tuple = date.timetuple()
#                weekday = time_tuple.tm_wday
#                
#                if weekday >= 5:
#                    dc.SetBrush(wx.Brush(weekend_color))
#                else:
#                    dc.SetBrush(wx.Brush(background_color))
#                    
#                dc.DrawRectangle(x=ruler_x_pos + weekdaynumbers_offset[0], 
#                                 y=top_left_corner[1] + graph_offset[1] + (row*name_size[1]), 
#                                 width=day_size[0] + line_width, 
#                                 height=name_size[1] + line_width)
#                             
#            row += 1
            
    
    def get_weekday(self, date, string=True):
        time_tuple = date.timetuple()
        weekday = time_tuple.tm_wday
        
        if string == True:
            weekday = weekdays[weekday]  
        return weekday
    
    
    def center_text(self, dc, text='', size=(0,0)):
        text_size = dc.GetTextExtent(text)
        text_offset = ((size[0] - text_size[0]) / 2, ((size[1]-text_size[1]) / 2))
        return text_offset
        
        
        
class GanttChart(BufferedWindow):
    def __init__(self, parent, year, month, content=[]):
        ## Any data the Draw() function needs must be initialized before
        ## calling BufferedWindow.__init__, as it will call the Draw
        ## function.
        
        self.line_width = 1.0
        self.scale = 1.0
        self.year = year #2011
        self.month = month #5
        self.content = content
        
        BufferedWindow.__init__(self, parent, id=wx.ID_ANY)
        self.SetSize(parent.GetSize())

        
    def Draw(self, dc):        
        dc.SetBackground( wx.Brush("White") )
        dc.Clear() # make sure you clear the bitmap!
        #print 'zoom: %i' % int(self.scale*100)
        top_left_corner =     ( 10 * self.scale,  10 * self.scale)
        bottom_right_corner = (630 * self.scale, 470 * self.scale)
        
        day_size =  ( 20 * self.scale, 20 * self.scale)
        name_size = (100 * self.scale, 25 * self.scale)
        line_width = self.line_width * self.scale
        
        monthnames_row = 0
        calendarweeks_row = 1
        weekdaynumbers_row = 2
        weekdaynames_row = 3
        graph_row = 4
        
        first_weekday = calendar.monthrange(self.year, self.month)[0]
        number_of_monthdays = calendar.monthrange(self.year, self.month)[1]
        
        monthnames_offset = (name_size[0], monthnames_row * day_size[1])
        calendarweeks_offset = (name_size[0], calendarweeks_row * day_size[1])
        weekdaynumbers_offset = (name_size[0], weekdaynumbers_row * day_size[1])
        weekdaynames_offset = (name_size[0], weekdaynames_row * day_size[1])
        graph_offset = (0, graph_row * day_size[1])
        
        # draw top top ruler --------------------------------------------------
        dc.SetPen(wx.Pen(foreground_color, line_width))
        
        font_size = (day_size[0] / 2) * 0.8
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
            
                
            # Draw day by number
            dc.DrawRectangle(x=ruler_x_pos + weekdaynumbers_offset[0], 
                             y=top_left_corner[1] + weekdaynumbers_offset[1], 
                             width=day_size[0] + line_width, 
                             height=day_size[1] + line_width)
                             
            text_offset = self.center_text(dc, str(day), day_size)
            dc.DrawText(text=str(day), 
                        x=ruler_x_pos + text_offset[0] + weekdaynumbers_offset[0],
                        y=top_left_corner[1] + text_offset[1] + weekdaynumbers_offset[1])
            
                            
            # Draw calendar-week
            if weekday == 0:
                cal_week_start_xpos = ruler_x_pos 
            if weekday == 6 or day == number_of_monthdays:
                dc.DrawRectangle(x=cal_week_start_xpos + calendarweeks_offset[0], 
                                 y=top_left_corner[1] + calendarweeks_offset[1], 
                                 width=(day_size[0] * (weekday+1)) + line_width, 
                                 height=day_size[1] + line_width)
                                 
                text_offset = self.center_text(dc, weekday_str, day_size)
                dc.DrawText(text='KW %i' % calendar_week,
                            x=cal_week_start_xpos + text_offset[0] + calendarweeks_offset[0], 
                            y=top_left_corner[1] + text_offset[1] + calendarweeks_offset[1])
                
            if weekday >= 5:
                dc.SetBrush(wx.Brush(weekend_color))
            else:
                dc.SetBrush(wx.Brush(background_color))
                
            # Draw day by weekday
            dc.DrawRectangle(x=ruler_x_pos + weekdaynames_offset[0], 
                             y=top_left_corner[1] + weekdaynames_offset[1], 
                             width=day_size[0] + line_width, 
                             height=day_size[1] + line_width)
                                              
            text_offset = self.center_text(dc, weekday_str, day_size)
            dc.DrawText(text=weekday_str, 
                        x=ruler_x_pos + text_offset[0] + weekdaynames_offset[0], 
                        y=top_left_corner[1] + text_offset[1] + weekdaynames_offset[1])
                        
            # Draw monthname
            if day == number_of_monthdays:
                dc.DrawRectangle(x=top_left_corner[0] + monthnames_offset[0], 
                                 y=top_left_corner[1] + monthnames_offset[1], 
                                 width=(day_size[0] * number_of_monthdays) + line_width, 
                                 height=day_size[1] + line_width)
                                 
                text_offset = self.center_text(dc, weekday_str, day_size)
                dc.DrawText(text='%s' % monthnames[self.month-1],
                            x=top_left_corner[0] + text_offset[0] + monthnames_offset[0], 
                            y=top_left_corner[1] + text_offset[1] + monthnames_offset[1])

            
        # Draw dudes
        row = 0
        for content in self.content:
            dc.DrawRectangle(x=top_left_corner[0] + graph_offset[0], 
                             y=top_left_corner[1] + graph_offset[1] + (row*name_size[1]), 
                             width=name_size[0] + line_width, 
                             height=name_size[1] + line_width)
                             
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
                                 width=day_size[0] + line_width, 
                                 height=name_size[1] + line_width)
                             
            row += 1
            
                    
    def center_text(self, dc, text='', size=(0,0)):
        text_size = dc.GetTextExtent(text)
        text_offset = ((size[0] - text_size[0]) / 2, ((size[1]-text_size[1]) / 2))
        return text_offset
        

        
# Just for test Purposes -------------------------------------------------------
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
