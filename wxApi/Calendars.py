# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wxApi.Calendars module.
# by Mark Muzenhardt, published under LGPL license.
#===============================================================================

import wx, wx.lib.dragscroller
import calendar, datetime, time

from decimal import Decimal
from pprint import pprint
from Widgets import BufferedWindow


WEEKEND_COLOR = '#FFAA00'
FOREGROUND_COLOR = 'black'
BACKGROUND_COLOR = 'white'
LIGHT_GREY = '#A4A4A4'

WEEKDAYS = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
WEEKDAYS_ABBREVATION = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
MONTHNAMES = ['Januar', 'Februar', u'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
MONTHNAMES_ABBREVATION = ['Jan', 'Feb', 'Mrz', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
        

class DayChart(object):
    def __init__(self, parent, id=wx.ID_ANY):
        self.parent = parent
        
        sizer_main = wx.FlexGridSizer( 2, 1, 0, 0 )
        sizer_main.AddGrowableCol( 0 )
        sizer_main.AddGrowableRow( 1 )
        self.parent.SetSizer( sizer_main )
        
        
        self.panel_header = wx.Panel( self.parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.sizer_panel_header = wx.BoxSizer(wx.VERTICAL)
        self.panel_header.SetSizer(self.sizer_panel_header)
        
        self.day_header = DayHeader(self.panel_header)
        self.sizer_panel_header.Add(self.day_header, 1, wx.EXPAND)
        sizer_main.Add( self.panel_header, 1, wx.EXPAND) # |wx.ALL, 5 )
        
        self.panel_grid = wx.Panel( self.parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.sizer_panel_grid = wx.BoxSizer(wx.VERTICAL)
        self.panel_grid.SetSizer(self.sizer_panel_grid)
        
        self.day_grid = DayGrid(self.panel_grid)
        self.sizer_panel_grid.Add(self.day_grid, 1, wx.EXPAND)
        sizer_main.Add( self.panel_grid, 1, wx.EXPAND) # |wx.ALL, 5 )

        #self.parent.SetWindowStyle(wx.HSCROLL)
        #self.parent.SetVirtualSize((3000, 3000))
        #self.parent.SetScrollbar(wx.VSCROLL, 0, 400, 3000)
        
        self.parent.Layout()
        
        
    def set_date_range(self, start_date=None, end_date=None, nof_days=None):
        self.day_header.set_date_range(start_date, end_date, nof_days)
        self.day_grid.set_date_range(start_date, end_date, nof_days)



class DayHeader(BufferedWindow):
    def __init__(self, parent):
        self.parent = parent
        
        self.start_date = None
        self.end_date = None
        
        self._line_width = 1.0
        self._parent_size = self.parent.GetSize()
        self._top_left_corner =     ( 10,  10)
        self._bottom_right_corner = (self._parent_size[0] - 10, self._parent_size[1] - 10)
        self._clocktime_size = (100, 50)
        self._day_size = (200, 50)
        self._graph_row = 2
        self._mouse_pos = (0, 0)
        
        BufferedWindow.__init__(self, parent, id=wx.ID_ANY)
        self.SetSize((1400, (self._day_size[1]*2) + self._top_left_corner[1]))
        
        #self.Bind(wx.EVT_PAINT, self.on_paint)
        #self.parent.Bind(wx.EVT_SIZE, self.on_size)
                
        
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
    
    
    def Draw(self, dc): #event=None):
        #dc = wx.PaintDC(self)
        self.DoPrepareDC(dc)
        dc.Clear()
        
        if self.start_date == None or self.end_date == None:
            return
        
        #monthnames_row = 0
        weekdaynumbers_row = 0
        weekdaynames_row = 1
        
        #monthnames_offset = (clocktime_size[0], monthnames_row * day_size[1])
        weekdaynumbers_offset = (self._clocktime_size[0], weekdaynumbers_row * self._day_size[1])
        weekdaynames_offset = (self._clocktime_size[0], weekdaynames_row * self._day_size[1])
        graph_offset = (0, self._graph_row * self._day_size[1])
        
        # draw top top ruler --------------------------------------------------
        dc.SetPen(wx.Pen(FOREGROUND_COLOR, self._line_width))
        
        if self._day_size[0] > self._day_size[1]:
            smaller_size = self._day_size[1]
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
            month = day_date.month
            year = day_date.year
            weekday = self.get_weekday(date=day_date, string=False)
            weekday_str = self.get_weekday(date=day_date, string=True)
            
            ruler_x_pos = self._top_left_corner[0] + ((day_delta) * self._day_size[0])
            dc.SetBrush(wx.Brush('white'))
            
            if cal_week_start_xpos == None:
                cal_week_start_xpos = ruler_x_pos
            
            # Draw year
            pass
            
            if weekday >= 5:
                dc.SetBrush(wx.Brush(WEEKEND_COLOR))
                    
            # Draw day by number
            dc.DrawRectangle(x=ruler_x_pos + weekdaynumbers_offset[0], 
                             y=self._top_left_corner[1] + weekdaynumbers_offset[1], 
                             width=self._day_size[0] + self._line_width, 
                             height=self._day_size[1] + self._line_width)
                             
            text_offset = self.center_text(dc, str(day), self._day_size)
            dc.DrawText(text=str(day), 
                        x=ruler_x_pos + text_offset[0] + weekdaynumbers_offset[0],
                        y=self._top_left_corner[1] + text_offset[1] + weekdaynumbers_offset[1])
                
            # Draw day by weekday
            dc.DrawRectangle(x=ruler_x_pos + weekdaynames_offset[0], 
                             y=self._top_left_corner[1] + weekdaynames_offset[1], 
                             width=self._day_size[0] + self._line_width, 
                             height=self._day_size[1] + self._line_width)
                                              
            text_offset = self.center_text(dc, weekday_str, self._day_size)
            dc.DrawText(text=weekday_str, 
                        x=ruler_x_pos + text_offset[0] + weekdaynames_offset[0], 
                        y=self._top_left_corner[1] + text_offset[1] + weekdaynames_offset[1])
                        
            dc.SetBrush(wx.Brush(BACKGROUND_COLOR))
            
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
        
        
    def get_weekday(self, date, string=True):
        time_tuple = date.timetuple()
        weekday = time_tuple.tm_wday
        
        if string == True:
            weekday = WEEKDAYS[weekday]  
        return weekday
    
    
    def center_text(self, dc, text='', size=(0,0)):
        text_size = dc.GetTextExtent(text)
        text_offset = ((size[0] - text_size[0]) / 2, ((size[1]-text_size[1]) / 2))
        return text_offset
    
    
    
class DayGrid(BufferedWindow):
    def __init__(self, parent):
        self.parent = parent
        self.start_date = None
        self.end_date = None
        
        #self.start_time = None
        #self.end_time = None
        self._line_width = 1.0
        
        self._parent_size = self.parent.GetSize()
        self._top_left_corner =     ( 10,  0)
        self._bottom_right_corner = (self._parent_size[0] - 10, self._parent_size[1] - 10)
        self._clocktime_size = (100, 50)
        self._day_size =  (200, 50)
        self._graph_row = 0
        self._mouse_pos = (0, 0)
        
        # No, I do not know why the SetScrollbars parameters are calculated this way!
        BufferedWindow.__init__(self, parent, id=wx.ID_ANY)
        self.SetScrollbars(0, self._day_size[1] / 4, 0, (24 * self._day_size[1]) / (self._day_size[1] / 4), 0, 0)
        
        self.Bind(wx.EVT_LEFT_DOWN, self.on_mouse_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_mouse_left_up)
        self.Bind(wx.EVT_MOTION, self.on_mouse_moved)
        
        
    def on_mouse_left_down(self, event):
        self._clicked_day = self._get_daydelta(self._mouse_pos)
        self._clicked_time = self._get_time(self._mouse_pos)
        print 'conversion:', self._clicked_time
        
        
    def on_mouse_left_up(self, event):
        self._released_day = self._get_date(self._mouse_pos)
        self._released_time = self._get_time(self._mouse_pos)
        print 'released left on button on day %s, time %s' % (str(self._released_day), str(self._released_time))
        
        
    def on_mouse_moved(self, event):
        self._mouse_pos = self.CalcUnscrolledPosition(event.GetPositionTuple())
        self.SetFocus()
        
        if event.Dragging():
            self._dragging_day = self._get_daydelta(self._mouse_pos)
            self._dragging_time = self._get_time(self._mouse_pos)
            print 'dragging over day %s, time %s' % (str(self._dragging_day), str(self._dragging_time))


    def get_date_pos(self, date):
        x1=None
        x2=None
        return x1, x2
        
    
    def get_time_pos(self, time):
        y1 = None
        y2 = None
        return y1, y2
    
    
    def _get_date(self, pos_tuple):
        daydelta = self._get_daydelta(pos_tuple)
        date = self.start_date + datetime.timedelta(days=daydelta)
        return date
    
    
    def _get_daydelta(self, pos_tuple):
        day = None
        if self._mouse_pos[0] >= (self._clocktime_size[0] + self._top_left_corner[0]):
            day = (self._mouse_pos[0] - self._clocktime_size[0] - self._top_left_corner[0]) / self._day_size[0]
        return day
    
    
    def _get_time(self, pos_tuple):
        dectime = None
        if self._mouse_pos[1] >= (self._top_left_corner[1] + (self._graph_row * self._day_size[1])):
            dectime = float(self._mouse_pos[1] - (self._graph_row * self._day_size[1]) - self._top_left_corner[1]) / self._day_size[1]
        time = self.dec_to_time(dectime)
        time = self.round_time(time)
        return time
    
    
    def round_time(self, time):
        hour = time.hour
        minute = time.minute
        
        for c in xrange(0, 75, 15):
            if minute > c:
                continue
            else:
                minute = c - 15
                break
        
        if minute <= 0:
            minute = 0
            
        time = datetime.time(hour, minute)
        return time
        
        
    def add_appointment(self, title, day, start_time, end_time):
        pass
    
    
    def mark_timerange(self):
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
    
    
    def Draw(self, dc): #event=None):
        #dc = wx.PaintDC(self)
        self.DoPrepareDC(dc)
        
        #dc.SetBackground(wx.Brush("White"))
        dc.Clear()
        
        if self.start_date == None or self.end_date == None:
            return
        
        #monthnames_row = 0
        weekdaynumbers_row = 0
        #weekdaynames_row = 1
        
        #monthnames_offset = (clocktime_size[0], monthnames_row * day_size[1])
        weekdaynumbers_offset = (self._clocktime_size[0], weekdaynumbers_row * self._day_size[1])
        #weekdaynames_offset = (self._clocktime_size[0], weekdaynames_row * self._day_size[1])
        graph_offset = (0, self._graph_row * self._day_size[1])
        
        # draw top top ruler --------------------------------------------------
#        dc.SetPen(wx.Pen(FOREGROUND_COLOR, self._line_width))
#        
        if self._day_size[0] > self._day_size[1]:
            smaller_size = self._day_size[1]
        font_size = (smaller_size / 2) * 0.6
        font = wx.Font(pointSize=font_size,
                       family=wx.FONTFAMILY_DEFAULT,
                       style=wx.FONTSTYLE_NORMAL, 
                       #face='Lucida Console', 
                       weight=wx.FONTWEIGHT_NORMAL)
        dc.SetFont(font)
#        
        end_delta = self.end_date - self.start_date

        # Draw timing...
        row = 0
        for hour in xrange(0, 24):
            time = datetime.time(hour=hour)
            time_str = time.strftime('%H:%M')
            
            dc.DrawRectangle(x=self._top_left_corner[0] + graph_offset[0], 
                             y=self._top_left_corner[1] + graph_offset[1] + (row*self._clocktime_size[1]), 
                             width=self._clocktime_size[0] + self._line_width, 
                             height=self._clocktime_size[1] + self._line_width)
                             
            text_offset = self.center_text(dc, time_str, self._clocktime_size)
            dc.DrawText(text=time_str, 
                        x=self._top_left_corner[0] + text_offset[0], 
                        y=self._top_left_corner[1] + text_offset[1] + graph_offset[1] + (row*self._clocktime_size[1]))
            
            for day_delta in xrange(0, end_delta.days + 1):
                day_date = self.start_date + datetime.timedelta(days=day_delta)
                day = day_date.day
                ruler_x_pos = self._top_left_corner[0] + ((day_delta) * self._day_size[0])
                weekday =self.get_weekday(date=day_date, string=False)
                
                if weekday >= 5:
                    dc.SetBrush(wx.Brush(WEEKEND_COLOR))
                    
                dc.DrawRectangle(x=ruler_x_pos + weekdaynumbers_offset[0], 
                                 y=self._top_left_corner[1] + graph_offset[1] + (row*self._clocktime_size[1]), 
                                 width=self._day_size[0] + self._line_width, 
                                 height=self._clocktime_size[1] + self._line_width)
                
                # Draw dashed quarters
                dc.SetPen(wx.Pen(LIGHT_GREY, self._line_width, wx.DOT))
                for quarter in xrange(1, 4):
                    dc.DrawLine(ruler_x_pos + weekdaynumbers_offset[0],                     self._top_left_corner[1] + graph_offset[1] + (row*self._clocktime_size[1]) + ((self._day_size[1] / 4) * quarter) + self._line_width, 
                                ruler_x_pos + weekdaynumbers_offset[0] + self._day_size[0], self._top_left_corner[1] + graph_offset[1] + (row*self._clocktime_size[1]) + ((self._day_size[1] / 4) * quarter) + self._line_width)
                
                dc.SetPen(wx.Pen(FOREGROUND_COLOR, self._line_width, wx.SOLID))    
                dc.SetBrush(wx.Brush(BACKGROUND_COLOR))
            row += 1
            
            
    def draw_appointments(self, appointments):
        ''' appointments is a list of dictionarys, which has that layout:
            [{'id': 0, 'title: 'Dentist, 'start_time': <datetime_object>, 'end_time': <datetime_object>}] '''
            
        for appointment_dict in appointments:
            pass
        
        
    def get_weekday(self, date, string=True):
        time_tuple = date.timetuple()
        weekday = time_tuple.tm_wday
        
        if string == True:
            weekday = WEEKDAYS[weekday]  
        return weekday
    
    
    def dec_to_time(self, dectime):
        if dectime == None:
            return None
        
        hour=int(str(dectime).split('.')[0])
        
        dectime_str = Decimal(str(dectime))
        dectime_str = '%.2f' % dectime_str
        minute=Decimal(str(dectime_str).split('.')[1])*60
        minute=int(minute/100)
        
        time = datetime.time(hour, minute)
        return time
    
    
    def center_text(self, dc, text='', size=(0,0)):
        text_size = dc.GetTextExtent(text)
        text_offset = ((size[0] - text_size[0]) / 2, ((size[1]-text_size[1]) / 2))
        return text_offset
            
            

# GANTT charting technology ---------------------------------------------------
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
        #dc.Clear() # make sure you clear the bitmap!
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
        dc.SetPen(wx.Pen(FOREGROUND_COLOR, line_width))
        
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
            weekday_str = WEEKDAYS[weekday]
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
                dc.SetBrush(wx.Brush(WEEKEND_COLOR))
            else:
                dc.SetBrush(wx.Brush(BACKGROUND_COLOR))
                
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
                dc.DrawText(text='%s' % MONTHNAMES[self.month-1],
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
                    dc.SetBrush(wx.Brush(WEEKEND_COLOR))
                else:
                    dc.SetBrush(wx.Brush(BACKGROUND_COLOR))
                    
                dc.DrawRectangle(x=ruler_x_pos + weekdaynumbers_offset[0], 
                                 y=top_left_corner[1] + graph_offset[1] + (row*name_size[1]), 
                                 width=day_size[0] + line_width, 
                                 height=name_size[1] + line_width)
                             
            row += 1
            
                    
    def center_text(self, dc, text='', size=(0,0)):
        text_size = dc.GetTextExtent(text)
        text_offset = ((size[0] - text_size[0]) / 2, ((size[1]-text_size[1]) / 2))
        return text_offset
        

