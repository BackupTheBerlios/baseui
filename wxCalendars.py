# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wxCalendars module.
# by Mark Muzenhardt, published under LGPL license.
#===============================================================================

from wxApi import Calendars
from ContentDefinitionBase import TableContentBase
from pprint import pprint


class DayChart(Calendars.DayChart, TableContentBase):
    def __init__(self, parent, db_table=None, form_class=None, remote_parent=None):
        Calendars.DayChart.__init__(self, parent)
        
        self.day_grid.open_appointment = self.on_open_appointment
        
        self.db_table = db_table
        self.form = form_class
        self.remote_parent = remote_parent
        self.primary_key = None
        
    
    def on_populate(self, data=None):
        pk = self.remote_parent.primary_key
        if pk <> None:
            self.populate()
        else:
            # Disable calendar when remote_parent has no pk (f.e. new dataset on remote).
            self.panel_grid.Enable(False)
            self.panel_header.Enable(False)
        
    
    def on_open_appointment(self, appointment_dict):
        if self.form <> None:
            form_instance = self.form(parent=self.parent, remote_parent=self, permissions={}) #self.form_permissions)
            form_instance.populate(appointment_dict)
        else:
            print 'No form defined!'


    def populate(self, data=None):
        print 'POPULATE', data, self.day_grid.appointments_lod
        
        
        
        
