# -*- coding: iso-8859-1 -*-

#===============================================================================
# GTKapi Menus module.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import gtk, gobject


class Bar:
    ''' Made to create simple menu bars. '''

    # Example ------------------------------------------------------------------
    menu_definition = [{'item_name': 'Datenbank', 'icon': None, '#child':
                            [
                            {'item_name': 'hinzufügen', 'icon': None, 'on_click': self.Database.add()},
                            {'item_name': 'entfernen', 'icon':None, 'on_click': self.Database.delete()}
                            ]
                      }]



class Button:
    ''' Draws button menus. '''
    pass



class Context:
    ''' Draws context menus. '''
    
    def __init__(self, widget, encoding='latin-1'):
        pass
        



class Accordian:
    ''' Draws accordian menus. '''
    pass



