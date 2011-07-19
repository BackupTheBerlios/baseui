# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wxCalendars module.
# by Mark Muzenhardt, published under LGPL license.
#===============================================================================

from wxApi import Calendars
from pprint import pprint


class DayChart(Calendars.DayChart):
    def __init__(self, parent, db_table=None, form_class=None, remote_parent=None):
        Calendars.DayChart.__init__(self, parent)
        
        self.day_grid.open_appointment = self.on_open_appointment
        self.db_table = db_table
        self.form = form_class
        self.remote_parent = remote_parent
        self.primary_key = None
        
        
    def on_save(self, data):
        print 'saving calendar,', data
        pprint(self.day_grid.appointments_lod)
        
        
    def on_delete(self, data):
        print 'delete calendar', data
        
        
    def on_populate(self, primary_key):
        #self.primary_key = primary_key.primary_key
        #print 'populating calendar', self.primary_key, primary_key.db_table
        #print self.parent
        pass
        
    
    def on_open_appointment(self, appointment_dict):
        if self.form <> None:
            form_instance = self.form(parent=self.parent, remote_parent=self, permissions={}) #self.form_permissions)
            form_instance.populate(appointment_dict)
        else:
            print 'No form defined!'



