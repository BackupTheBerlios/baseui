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
from Dialogs import Error


WEEKEND_COLOR = '#AADDFF'
FOREGROUND_COLOR = 'black'
BACKGROUND_COLOR = 'white'
LIGHT_GREY = '#A4A4A4'
MARKER_COLOR = '#6699FF'
APPOINTMENT_COLOR = '#2255FF'

WEEKDAYS = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
WEEKDAYS_ABBREVATION = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
MONTHNAMES = ['Januar', 'Februar', u'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
MONTHNAMES_ABBREVATION = ['Jan', 'Feb', 'Mrz', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
        

class CalendarBase(BufferedWindow):
    def __init__(self, parent):
        self.parent = parent
        
        self.start_date = None
        self.end_date = None
        
        self._line_width = 1.0
        self._parent_size = self.parent.GetSize()
        self._top_left_corner =     ( 10,  10)
        self._bottom_right_corner = (self._parent_size[0] - 10, self._parent_size[1] - 10)
        self._clocktime_size = (100, 40)
        self._day_size = (200, 50)
        self._graph_row = 2
        self._mouse_pos = (0, 0)
        
        BufferedWindow.__init__(self, parent, id=wx.ID_ANY)
        self.dialog_error = Error(parent)
        

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
    
    
    def adjust_font(self, dc, size, font=None):
        face = font
        
        if size[0] > size[1]:
            smaller_size = size[1]
        else:
            smaller_size = size[0]
            
        font_size = (smaller_size / 2) * 0.6
        
        font_dict = {}
        font_dict['pointSize'] = font_size
        font_dict['family'] = wx.FONTFAMILY_DEFAULT
        font_dict['style'] = wx.FONTSTYLE_NORMAL
        if face <> None:
            font_dict['face'] = face, 
        font_dict['weight'] = wx.FONTWEIGHT_NORMAL
                       
        font = wx.Font(**font_dict)
        dc.SetFont(font)
    
    
    def get_date_pos(self, date):
        delta = date-self.start_date
        day_delta = delta.days
        
        x1 = self._top_left_corner[0] + self._clocktime_size[0] + (self._day_size[0] * day_delta)
        x2 = x1 + self._day_size[0]
        return x1, x2
        
    
    def get_time_pos(self, time, mins=True):
        rounded_time = self.round_time(time, round_down=False)
        hour = rounded_time.hour
        minute = rounded_time.minute
        
        if mins == True:
            minute_offset = int(self._clocktime_size[1] * (minute / float(60)))
        else:
            minute_offset = self._clocktime_size[1]
            
        y1 = self._top_left_corner[1] + (self._clocktime_size[1] * hour)
        y2 = y1 + minute_offset
        return y1, y2
    
    
    def get_datetime_pos(self, dt):
        time = datetime.time(dt.hour, dt.minute, dt.second)
        date = datetime.date(dt.year, dt.month, dt.day)
        
        x1, x2 = self.get_date_pos(date)
        y1, y2 = self.get_time_pos(time)
        return x1, y1, x2, y2
    
    
    def get_date(self, pos_tuple):
        daydelta = self.get_daydelta(pos_tuple)
        date = self.start_date + datetime.timedelta(days=daydelta)
        return date
    
    
    def get_daydelta(self, pos_tuple):
        day = None
        if self._mouse_pos[0] >= (self._clocktime_size[0] + self._top_left_corner[0]):
            day = (self._mouse_pos[0] - self._clocktime_size[0] - self._top_left_corner[0]) / self._day_size[0]
        return day
    
    
    def get_time(self, pos_tuple):
        dectime = None
        if self._mouse_pos[1] >= (self._top_left_corner[1] + (self._graph_row * self._clocktime_size[1])):
            dectime = float(self._mouse_pos[1] - (self._graph_row * self._clocktime_size[1]) - self._top_left_corner[1]) / self._clocktime_size[1]
        time = self.dec_to_time(dectime)
        time = self.round_time(time)
        return time
    
    
    def get_datetime(self, pos_tuple):
        date = self.get_date(pos_tuple)
        time = self.get_time(pos_tuple)
        dt = datetime.datetime(date.year, date.month, date.day, time.hour, time.minute, time.second)
        return dt
    
        
    def round_time(self, time, round_down=True):
        hour = time.hour
        minute = time.minute
        
        for c in xrange(0, 75, 15):
            if minute > c:
                continue
            else:
                if round_down == True:
                    minute = c - 15
                else:
                    minute = c
                break
        
        if minute <= 0:
            minute = 0
            
        time = datetime.time(hour, minute)
        return time
    
    
        
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



class DayHeader(CalendarBase):
    def __init__(self, parent):
        CalendarBase.__init__(self, parent)
        self.SetSize((1400, (self._day_size[1]*2) + self._top_left_corner[1]))
        
        
    def Draw(self, dc): #event=None):        
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
        self.adjust_font(dc, self._day_size)
        
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



class DayGrid(CalendarBase):
    ID_EDIT = 101
    ID_DELETE = 102
    
    def __init__(self, parent):
        CalendarBase.__init__(self, parent)
        
        self.start_date = None
        self.end_date = None
        
        #self.start_time = None
        #self.end_time = None
        self._line_width = 1.0
        
        self._parent_size = self.parent.GetSize()
        self._top_left_corner =     ( 10,  0)
        self._bottom_right_corner = (self._parent_size[0] - 10, self._parent_size[1] - 10)
        
        self._marker_starts = None
        self._marker_ends = None
        self._move_tracker_starts = None
        self._move_tracker_ends = None
        
        self._hovering_dict = None
        self._move_appointment = None
        self._start_resize_dict = None
        self._start_resize_appointment = None
        self._end_resize_dict = None
        self._end_resize_appointment = None
        
        self._resize_edge = 4 # even value because divided by 2
        
        self.appointments_lod = []
        
        self._graph_row = 0
        self._mouse_pos = (0, 0)
        
        self._left_down = False
        
        # No, I do not know why the SetScrollbars parameters are calculated this way!
        self.SetScrollbars(0, self._clocktime_size[1] / 4, 0, (24 * self._clocktime_size[1]) / (self._clocktime_size[1] / 4), 0, 0)
        
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse_events)
        
        
    def on_mouse_events(self, event):
        self._mouse_pos = self.CalcUnscrolledPosition(event.GetPositionTuple())
        event.Skip()
        
        left_border = self.get_date_pos(self.start_date)[0]
        right_border = self.get_date_pos(self.end_date)[1]
        
        # If the mouse cursor is off the border, do nothing.
        if event.Leaving() or \
           self._mouse_pos[0] < left_border or \
           self._mouse_pos[0] > right_border:
            self.reset_tracker()
            self.reset_marker()
            return
        
        self.check_hovering()
        
        if event.LeftDown():
            self._left_down = True
            self._clicked_datetime = self.get_datetime(self._mouse_pos)
            
            if self._hovering_dict <> None:
                self._move_appointment = self._hovering_dict
                
            if self._start_resize_dict <> None:
                self._start_resize_appointment = self._start_resize_dict
                print 'start_resize begins'
                
            if self._end_resize_dict <> None:
                self._end_resize_appointment = self._end_resize_dict
                print 'end_resize begins'
                
        if event.LeftDClick():
            self.open_appointment(self._hovering_dict)
            
        if event.LeftUp():
            self._left_down = False
            self._released_datetime = self.get_datetime(self._mouse_pos)
                
            if self._move_appointment == None and \
               self._start_resize_appointment == None and \
               self._end_resize_appointment == None:
                try:
                    self.add_appointment(title='foggie', start_datetime=self._clicked_datetime, end_datetime=self._released_datetime)
                except Exception, inst:
                    self.dialog_error.show(instance=inst, message=u'Fehler beim hinzufügen eines Termins.')
            
            delta = self._released_datetime - self._clicked_datetime
            if self._move_appointment <> None:
                self.move_appointment(delta)
                        
            if self._start_resize_appointment <> None:
                self.resize_appointment(delta) #print 'start resize ends!'
                self._start_resize_appointment = None
            
            if self._end_resize_appointment <> None:
                self.resize_appointment(delta)
                self._end_resize_appointment = None
                
        if event.RightDown():
            if self._hovering_dict <> None:
                self.on_appointment_right_clicked()
                
        if event.Dragging() and self._left_down:
            self._dragging_datetime = self.get_datetime(self._mouse_pos)
            
            if self._move_appointment == None and \
               self._start_resize_appointment == None and \
               self._end_resize_appointment == None:
                self.mark_timerange(self._clicked_datetime, self._dragging_datetime)
            
            if self._move_appointment <> None:
                self.track_move(self._dragging_datetime - self._clicked_datetime)
        
            if self._start_resize_appointment <> None:
                self.track_start_resize(self._dragging_datetime - self._clicked_datetime)
                
            if self._end_resize_appointment <> None:
                self.track_end_resize(self._dragging_datetime - self._clicked_datetime)
        
    
    def create_context_menu(self):
        context_menu = wx.Menu()
        context_menu.Append(self.ID_EDIT, u"Öffnen")
        context_menu.Bind(wx.EVT_MENU, self.on_open_appointment, id=self.ID_EDIT)
        context_menu.Append(self.ID_DELETE, "Löschen")
        context_menu.Bind(wx.EVT_MENU, self.on_remove_appointment, id=self.ID_DELETE)
        return context_menu
        
        
    def on_open_appointment(self, event=None):
        self.open_appointment(self._hovering_dict)
        
        
    def on_appointment_right_clicked(self):
        self.PopupMenu(self.create_context_menu())
        
        
    def on_remove_appointment(self, event=None):
        self.appointments_lod.remove(self._hovering_dict)
        self.reset_marker()
        
        
    def check_overlap(self, start_dt=None, end_dt=None, exclude=None):
        for appointment_dict in self.appointments_lod:
            if exclude == appointment_dict:
                continue
            
            starts = appointment_dict.get('starts')
            ends = appointment_dict.get('ends')
            
            # Check if overlapping.
            if start_dt > starts and start_dt < ends or \
               start_dt < starts and end_dt > ends or \
               end_dt > starts and start_dt < starts:
                return False
        return True
    
                
    def check_hovering(self):
        hovering_dict = None
        start_resize_dict = None
        end_resize_dict = None
        
        got_it = False
        for appointment_dict in self.appointments_lod:
            starts = appointment_dict.get('starts')
            ends = appointment_dict.get('ends')
            
            start_coords = self.get_datetime_pos(starts)
            end_coords = self.get_datetime_pos(ends)
            
            # Check hovering between the x-axis    
            if self._mouse_pos[0] > start_coords[0] and \
               self._mouse_pos[0] < start_coords[2]:
                # Check hovering between the y-axis
                if self._mouse_pos[1] >= start_coords[3] + self._resize_edge and \
                   self._mouse_pos[1] <= end_coords[3] - self._resize_edge:
                    hovering_dict = appointment_dict
                    got_it = True
                    
                # Check hovering on upper edge to resize
                if self._mouse_pos[1] > start_coords[3] - self._resize_edge and \
                   self._mouse_pos[1] < start_coords[3] + self._resize_edge:
                    start_resize_dict = appointment_dict
                    got_it = True
                    
                # Check hovering on lower edge to resize
                if self._mouse_pos[1] > end_coords[3] - self._resize_edge and \
                   self._mouse_pos[1] < end_coords[3] + self._resize_edge:
                    end_resize_dict = appointment_dict
                    got_it = True
                
                # No need to continue if one dict has been found!
                if got_it == True:
                    break
        
        if hovering_dict <> None:
            self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
            self.UpdateDrawing()
        else:
            if self._hovering_dict <> None:
                #self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
                self._hovering_dict = hovering_dict
                self.UpdateDrawing()
                
        if start_resize_dict <> None or end_resize_dict <> None:
            self.SetCursor(wx.StockCursor(wx.CURSOR_SIZENS))
        
        if got_it == False:
            self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
            
        self._hovering_dict = hovering_dict
        self._start_resize_dict = start_resize_dict
        self._end_resize_dict = end_resize_dict
            
            
    def add_appointment(self, title, start_datetime, end_datetime):
        if start_datetime > end_datetime:
            start_datetime, end_datetime = end_datetime, start_datetime
        
        if start_datetime <> end_datetime:
            if start_datetime.day == end_datetime.day: 
                if self.check_overlap(start_datetime, end_datetime):
                    self.appointments_lod.append({'title': 'Foggie', 'starts': start_datetime, 'ends': end_datetime})
                    self.UpdateDrawing()
                else:
                    self.reset_marker()
                    raise Exception(u'Termine dürfen sich nicht überschneiden!')
            else:
                raise Exception(u'Ein Termin darf sich nicht über mehrere Tage erstrecken!')
        else:
            pass
        
        
    def open_appointment(self, appointment_dict):
        print u'no form defined! can´t open', appointment_dict
            
            
    def track_move(self, delta):
        starts = self._move_appointment.get('starts')
        ends = self._move_appointment.get('ends')
        
        if (starts + delta).day == (ends + delta).day:
            self._move_tracker_starts = self.get_datetime_pos(starts + delta)
            self._move_tracker_ends = self.get_datetime_pos(ends + delta)
        self.UpdateDrawing()
        
        
    def reset_tracker(self):
        self._move_appointment = None
        self._move_tracker_starts = None
        self._move_tracker_ends = None
        
        self._start_resize_appointment = None
        self._end_resize_appointment = None
        self.UpdateDrawing()
        
        
    def move_appointment(self, delta):
        starts = self._move_appointment.get('starts')
        ends = self._move_appointment.get('ends')
        
        if self.check_overlap(starts + delta, ends + delta, self._move_appointment) and \
           (starts + delta).day == (ends + delta).day:
            self._move_appointment['starts'] += delta
            self._move_appointment['ends'] += delta          
        
        self.reset_tracker()
        self.reset_marker()
    
        
    def resize_appointment(self, delta):
        if self._start_resize_appointment <> None:
            self._start_resize_appointment['starts'] += delta
        if self._end_resize_appointment <> None:
            self._end_resize_appointment['ends'] += delta
        self.reset_tracker()
        
            
    def track_start_resize(self, delta):
        starts = self._start_resize_appointment.get('starts')
        ends = self._start_resize_appointment.get('ends')
        
        if (starts + delta).day == (ends).day:
            self._move_tracker_starts = self.get_datetime_pos(starts + delta)
            self._move_tracker_ends = self.get_datetime_pos(ends)
        self.UpdateDrawing()
    
    
    def track_end_resize(self, delta):
        starts = self._end_resize_appointment.get('starts')
        ends = self._end_resize_appointment.get('ends')
        
        if (starts).day == (ends + delta).day:
            self._move_tracker_starts = self.get_datetime_pos(starts)
            self._move_tracker_ends = self.get_datetime_pos(ends + delta)
        self.UpdateDrawing()
    
    
    def mark_timerange(self, start_datetime, dragged_datetime):
        self._marker_starts = self.get_datetime_pos(start_datetime)
        self._marker_ends = self.get_datetime_pos(dragged_datetime)
        self.UpdateDrawing()
        
        
    def reset_marker(self):
        self._marker_starts = None
        self._marker_ends = None
        self.UpdateDrawing()
        
        
    def Draw(self, dc):
        if self.start_date == None or self.end_date == None:
            return
        
        weekdaynumbers_row = 0
        
        #monthnames_offset = (clocktime_size[0], monthnames_row * day_size[1])
        weekdaynumbers_offset = (self._clocktime_size[0], weekdaynumbers_row * self._day_size[1])
        #weekdaynames_offset = (self._clocktime_size[0], weekdaynames_row * self._day_size[1])
        self.adjust_font(dc, self._clocktime_size)        
        end_delta = self.end_date - self.start_date

        # Draw timing...
        row = 0
        for hour in xrange(0, 24):
            time = datetime.time(hour=hour)
            time_str = time.strftime('%H:%M')
            
            dc.DrawRectangle(x=self._top_left_corner[0], 
                             y=self._top_left_corner[1] + (row*self._clocktime_size[1]), 
                             width=self._clocktime_size[0] + self._line_width, 
                             height=self._clocktime_size[1] + self._line_width)
                             
            text_offset = self.center_text(dc, time_str, self._clocktime_size)
            dc.DrawText(text=time_str, 
                        x=self._top_left_corner[0] + text_offset[0], 
                        y=self._top_left_corner[1] + text_offset[1] + (row*self._clocktime_size[1]))
            
            for day_delta in xrange(0, end_delta.days + 1):
                day_date = self.start_date + datetime.timedelta(days=day_delta)
                day = day_date.day
                ruler_x_pos = self._top_left_corner[0] + ((day_delta) * self._day_size[0])
                weekday =self.get_weekday(date=day_date, string=False)
                
                if weekday >= 5:
                    dc.SetBrush(wx.Brush(WEEKEND_COLOR))
                    
                dc.DrawRectangle(x=ruler_x_pos + weekdaynumbers_offset[0], 
                                 y=self._top_left_corner[1] + (row*self._clocktime_size[1]), 
                                 width=self._day_size[0] + self._line_width, 
                                 height=self._clocktime_size[1] + self._line_width)
                
                # Draw dashed quarters
                dc.SetPen(wx.Pen(LIGHT_GREY, self._line_width, wx.DOT))
                for quarter in xrange(1, 4):
                    dc.DrawLine(ruler_x_pos + weekdaynumbers_offset[0],                     self._top_left_corner[1] + (row*self._clocktime_size[1]) + ((self._clocktime_size[1] / 4) * quarter), 
                                ruler_x_pos + weekdaynumbers_offset[0] + self._day_size[0], self._top_left_corner[1] + (row*self._clocktime_size[1]) + ((self._clocktime_size[1] / 4) * quarter))
                
                dc.SetPen(wx.Pen(FOREGROUND_COLOR, self._line_width, wx.SOLID))    
                dc.SetBrush(wx.Brush(BACKGROUND_COLOR))
            row += 1
            
        if self._marker_starts <> None and self._marker_ends <> None:
            self.DrawMarker(dc)
            
        if self.appointments_lod <> []:
            self.DrawAppointments(dc)
            
        if self._start_resize_appointment <> None or self._end_resize_appointment <> None:
            self.DrawResizeMarker(dc)
            
        if self._move_tracker_starts <> None and self._move_tracker_ends <> None:
            self.DrawMoveTracker(dc)
            
            
    def DrawResizeMarker(self, dc):
        pass
    
    
    def DrawMoveTracker(self, dc):
        dc.SetPen(wx.Pen(FOREGROUND_COLOR, self._line_width * 3))
        dc.SetBrush(wx.Brush(BACKGROUND_COLOR))
        dc.DrawRectangle(x=self._move_tracker_starts[0], 
                         y=self._move_tracker_starts[3], 
                         width=self._move_tracker_ends[2] - self._move_tracker_starts[0] + self._line_width, 
                         height=self._move_tracker_ends[3] - self._move_tracker_starts[3] + self._line_width)
        
        
    def DrawMarker(self, dc):
        dc.SetBrush(wx.Brush(MARKER_COLOR))
        dc.DrawRectangle(x=self._marker_starts[0], 
                         y=self._marker_starts[3], 
                         width=self._marker_ends[2] - self._marker_starts[0] + self._line_width, 
                         height=self._marker_ends[3] - self._marker_starts[3] + self._line_width)
        
#        dc.SetTextForeground(BACKGROUND_COLOR)
#        self.adjust_font(dc, size=(30, 30))
#        dc.DrawText(text='%s - %s' % (start_dt.strftime('%H:%M'), end_dt.strftime('%H:%M')), 
#                    x=app_starts_pos[0] + 5, 
#                    y=app_starts_pos[3] + 5)
        
        
    def DrawAppointments(self, dc):
        dc.SetBrush(wx.Brush(APPOINTMENT_COLOR))
        for appointment_dict in self.appointments_lod:
            start_dt = appointment_dict.get('starts')
            end_dt = appointment_dict.get('ends')
            
            app_starts_pos = self.get_datetime_pos(start_dt)
            app_ends_pos = self.get_datetime_pos(end_dt)
            
            # Check hovering (!!!)
            if self._hovering_dict == appointment_dict:
                dc.SetPen(wx.Pen(FOREGROUND_COLOR, self._line_width * 3)) #, wx.DOT))
            else:
                dc.SetPen(wx.Pen(FOREGROUND_COLOR, self._line_width)) #, wx.DOT))
                
            dc.DrawRectangle(x=app_starts_pos[0], 
                             y=app_starts_pos[3], 
                             width =app_ends_pos[2] - app_starts_pos[0] + self._line_width, 
                             height=app_ends_pos[3] - app_starts_pos[3] + self._line_width)
            
            dc.SetTextForeground(BACKGROUND_COLOR)
            self.adjust_font(dc, size=(30, 30))
            dc.DrawText(text='%s - %s' % (start_dt.strftime('%H:%M'), end_dt.strftime('%H:%M')), 
                        x=app_starts_pos[0] + 5, 
                        y=app_starts_pos[3] + 5)
            

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
        

