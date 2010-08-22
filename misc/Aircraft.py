# -*- coding: cp1252 -*-

from pprint import pprint


class Aircraft:
    countrys = {
        'D': {'DE': 'Deutschland'},
        'F': {'DE': 'Frankreich'},
    }
    
    registration = {
        'DE': {
            'A':    {'description': {
                         'DE': 'Luftfahrzeuge > 20 t Höchstabfluggewicht'},
                     'minimum_takeoff_weight': 20000,
                     'maximum_takeoff_weight':  None,
                    },
            'B':    {'description': {
                         'DE': 'Luftfahrzeuge von 14–20 t Höchstabfluggewicht'},
                     'minimum_takeoff_weight': 14000,
                     'maximum_takeoff_weight': 20000,
                    }, 
            'C':    {'description': {
                         'DE': 'Luftfahrzeuge 5,7–14 t Höchstabfluggewicht'},
                     'minimum_takeoff_weight':  5700,
                     'maximum_takeoff_weight': 14000,
                    },
            'E':    {'description': {
                         'DE': 'einmotorige Flugzeuge bis 2 t Höchstabfluggewicht'},
                     'minimum_takeoff_weight':  None,
                     'maximum_takeoff_weight':  2000,
                    },
            'F':    {'description': {
                         'DE': 'einmotorige Flugzeuge von 2 bis 5,7 t Höchstabfluggewicht'},
                     'minimum_takeoff_weight':  2000,
                     'maximum_takeoff_weight':  5700,
                    },
            'G':    {'description': {
                         'DE': 'mehrmotorige Flugzeuge bis 2 t Höchstabfluggewicht'},
                     'minimum_takeoff_weight':  None,
                     'maximum_takeoff_weight':  2000,
                    }, 
            'H':    {'description': {
                         'DE': 'Hubschrauber'},
                     'minimum_takeoff_weight':  None,
                     'maximum_takeoff_weight':  None,
                    },
            'I':    {'description': {
                         'DE': 'mehrmotorige Flugzeuge von 2 bis 5,7 t Höchstabfluggewicht'},
                     'minimum_takeoff_weight':  2000,
                     'maximum_takeoff_weight':  5700,
                    },
            'K':    {'description': {
                         'DE': 'Motorsegler'},
                     'minimum_takeoff_weight':  None,
                     'maximum_takeoff_weight':  None,
                    }, 
            'L':    {'description': {
                         'DE': 'Luftschiffe'},
                     'minimum_takeoff_weight':  None,
                     'maximum_takeoff_weight':  None,
                    },
            'M':    {'description': {
                         'DE': 'einmotorige Ultraleichtflugzeuge bzw. Luftsportgeräte bis 472,5 kg Höchstabfluggewicht'},
                     'minimum_takeoff_weight':  None,
                     'maximum_takeoff_weight':   472.5,
                    },
            'N':    {'description': {
                         'DE': 'nichtmotorisierte ultraleichte Segelflugzeuge, Hängegleiter und ähnliche'},
                     'minimum_takeoff_weight':  None,
                     'maximum_takeoff_weight':  None,
                    }, 
            'O':    {'description': {
                         'DE': 'Gas- und Heißluftballone'},
                     'minimum_takeoff_weight':  None,
                     'maximum_takeoff_weight':  None,
                    }, 
            '####': {'description': {
                         'DE': 'Segelflugzeuge'},
                     'minimum_takeoff_weight':  None,
                     'maximum_takeoff_weight':  None,
                    },
            },
        }
        
        
    def __init__(self):
        self.minimum_takeoff_weight = ''
        self.maximum_takeoff_weight = ''
        self.country = ''
        self.registration = ''
        
    
    def decode_registration(self, country, registration):
        ''' country = DE, FR, etc. as string,
            registration = EOMO, ENFR, KOEL, etc. as a string '''
            
        pass
        
        
if __name__ == "__main__":
    country =      raw_input('Country?      > ').upper()
    registration = raw_input('Registration? > ').upper()
    
    aircraft = Aircraft()
    pprint(aircraft.registration)
    
    print; raw_input('... give <RETURN> to exit')
        