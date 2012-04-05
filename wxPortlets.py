# -*- coding: iso-8859-1 -*-

#===============================================================================
# BaseUI.wxPortlets module.
# published under LGPL license by Mark Muzenhardt.
#===============================================================================



class PortletBase(object):
    ''' A so called "Portlet" basically consists of this things:
        - Menu
        - Toolbar
        - MainPanel '''
    
    def __init__(self, menu, toolbar, main_panel):
        self.menu = menu
        self.toolbar = toolbar
        self.main_panel = main_panel
        
        
    


#class DatabaseView(object):
    
    
    
    
#class Browser(object):



