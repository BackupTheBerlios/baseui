# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wxPortlets module.
# published under LGPL license by Mark Muzenhardt.
#===============================================================================



class PortletBase(object):
    ''' This class shall be used to create Outlook-styled applicatins. Email, 
        Calendar, Tasks, etc. are all Portlets there, which have their own
        Menu, Toolbar and MainPanel (and eventually a SidePanel) inside the 
        main application.'''
    
    
    def __init__(self, menu, toolbar, main_panel, side_panel):
        self.menu = menu
        self.toolbar = toolbar
        self.main_panel = main_panel
        self.side_panel = side_panel
        
    


#class DatabaseView(object):
    
    
    
    
#class Browser(object):



