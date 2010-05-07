# -*- coding: cp1252 -*-
# 
# http://weather.noaa.gov/pub/data/observations/metar/stations/EDDL.TXT

import urllib
from pprint import pprint


class Base:
    def __init__(self, url):
        self.url = url


    def download(self, station):
        full_url = self.url + station + '.TXT'
        file_object = urllib.urlopen(full_url)
        self.plaintext = file_object.read()


    def get_list(self):
        self.list = []
        tmp_list = self.plaintext.split('\n')

        for tmp_line in tmp_list:
            tmp_line_list = tmp_line.split(' ')
            while '' in tmp_line_list:
                tmp_line_list.remove('')
            self.list.append(tmp_line_list)
        return self.list        


        
class TAF(Base):
    duration = \
    {
        'BECMG': {'DE': 'dauerhafte Änderung',
                  'EN': 'becoming'},
        'TEMPO': {'DE': 'kurzzeitige Änderung',
                  'EN': 'temporary'}
    }

    weather_appearance = \
    {
        'BR': {'DE': 'feuchter Dunst',
               'EN': 'brume'},
        'DS': {'DE': 'Staubsturm',
               'EN': 'dust storm'},
        'DU': {'DE': 'Staub',
               'EN': 'dust'},
        'DZ': {'DE': 'Sprühregen',
               'EN': 'drizzle'},
        'FG': {'DE': 'Nebel',
               'EN': 'fog'},
        'FU': {'DE': 'Rauch',
               'EN': 'fume'},
        'GR': {'DE': 'Graupel oder Hagel',
               'EN': 'grail'},
        'GS': {'DE': 'kleiner Hagel (Graupelschauer)',
               'EN': 'sleet'},
        'HZ': {'DE': 'trockener Dunst',
               'EN': 'haze'},
        'PL': {'DE': 'Eiskörner',
               'EN': 'ice pellets'},
        'RA': {'DE': 'Regen',
               'EN': 'rain'},
        'SA': {'DE': 'Sand',
               'EN': 'sand'},
        'SG': {'DE': 'Schneegriesel',
               'EN': 'snow grains'},
        'SN': {'DE': 'Schnee',
               'EN': 'snow'},
        'SS': {'DE': 'Sandsturm',
               'EN': 'sandstorm'}
    }

    detailed_desciption = \
    {
        'BC': {'DE': 'Bänke von ...',
               'EN': 'patches ...'},
        'DR': {'DE': 'treibender ...',
               'EN': 'low drifting ...'},
        'FZ': {'DE': 'gefrierender ... ',
               'EN': 'freezing ...'},
        'MI': {'DE': 'flacher ... ',
               'EN': 'shallow ...'},
        'RE': {'DE': 'in der letzten Stunde, aber nicht zur Beobachtungszeit'},
        'SH': {'DE': 'Schauer',
               'EN': 'shower'},
        'TS': {'DE': 'Gewitter',
               'EN': 'thunderstorm'},
        'XX': {'DE': 'schwerer ...'}
    }

    clouds = \
    {
        'SKC': {'DE': 'wolkenlos',
                'EN': 'sky clear'},
        'CLR': {'DE': 'wolkenlos',
                'EN': 'sky clear'},
        'FEW': {'DE': 'wenige (1/8 - 2/8)',
                'EN': 'few (1/8 - 2/8)'},
        'SCT': {'DE': 'vereinzelt (3/8 - 4/8)',
                'EN': 'scattered (3/8 - 4/8)'},
        'BKN': {'DE': 'unterbrochen (5/8 - 7/8)',
                'EN': 'broken (5/8 - 7/8)'},
        'OVC': {'DE': 'bedeckt (8/8)',
                'EN': 'overcast (8/8)'},
        'CB':  {'DE': 'Gewitterwolken (Cumulonimbus)',
                'EN': 'thundery clouds (Cumulonimbus)'},
        'NSC': {'DE': 'nur Wolken in oder über 5000 ft, kein CB',
                'EN': 'nil significant cloud'}
    }

    descriptors = \
    {
        'CAVOK': {'DE': 'ceiling and Visibility OK'},
        'MPS':   {'DE': 'Meter pro Sekunde (meters per second)'},
        'KMH':   {'DE': 'Kilometer pro Stunde (kilometers per hour)'},
        'KT':    {'DE': 'Knoten = 1 Seemeile pro Stunde (Knots)'},
        'NSW':   {'DE': 'keine signifikante Wettererscheinung'},
        'PROB':  {'DE': 'Eintrittswahrscheinlichkeit der Vorhersage (Zahl in Prozent)'},
    }
        
    def __init__(self, url='http://weather.noaa.gov/pub/data/forecasts/taf/stations/'):
        Base.__init__(self, url)
        self.encoded_info_dict = {}
        self.encoded_forecast_dict = {}
        self.decoded_info_dict = {}
        self.decoded_forecast_dict = {}


    def get_encoded_info_dict(self):
        self.get_list()
        
        for tmp_line_list in self.list:
            if 'TAF' in tmp_line_list:
                taf_info_list = tmp_line_list
                self.encoded_info_dict = \
                {'ICAO':       taf_info_list[1],
                 'issued':     taf_info_list[2],
                 'timespan':   taf_info_list[3],
                 'wind':       taf_info_list[4],
                 'visibility': taf_info_list[5],
                 'clouds':     taf_info_list[6]}
        return self.encoded_info_dict


    def get_encoded_forecast_dict(self):
        self.get_list()
        duration_key_list = self.duration.keys()
        forecast_lol = []
        self.encoded_forecast_lod = []
        
        # Get forecast lol
        for tmp_line_list in self.list:
            for duration_key in duration_key_list:
                if duration_key in tmp_line_list:
                    forecast_lol.append(tmp_line_list)

        for taf_forecast_list in forecast_lol:
            tmp_forecast_dic = \
                {'duration': taf_forecast_list[0],
                 'validity_period': taf_forecast_list[1],
                 'detailed_description': self.identify(taf_forecast_list, 'detailed_description'),
                 'weather_appearance':   self.identify(taf_forecast_list, 'weather_appearance'),
                 'clouds':               self.identify(taf_forecast_list, 'clouds')}
            self.encoded_forecast_lod.append(tmp_forecast_dic)
        return self.encoded_forecast_lod

    
    def identify(self, forecast_list, tag):
        return None


    def get_decoded_info_dict(self, language='DE'):
        return


    def get_decoded_forecast_dict(self, language='DE'):
        return
            
            
                
class METAR(Base):
    qualifier_intensity = \
    {
        '-':  {'DE': 'schwach',
               'EN': 'light',
               'FR': 'faible'},
        ' ':  {'DE': 'mäßig',
               'EN': 'moderate',
               'FR': 'modéré'},
        '+':  {'DE': 'stark',
               'EN': 'heavy',
               'FR': 'forte'},
        'VC': {'DE': 'in der Nähe',
               'EN': 'in the Vicinity',
               'FR': 'au voisinage'},	
    }

    qualifier_descriptor = \
    {
        'MI': {'DE': 'flach',
               'EN': 'shallow',
               'FR': 'mince'}, 	
        'PR': {'DE': 'stellenweise',
               'EN': 'partial',
               'FR': 'partiel'}, 	
        'BC': {'DE': 'einzelne Schwaden',
               'EN': 'patches',
               'FR': 'bancs'}, 
        'DR': {'DE': 'fegend',
               'EN': 'low Drifting',
               'FR': 'chasse basse'},
        'BL': {'DE': 'treibend',
               'EN': 'blowing',
               'FR': 'chasse élevée'},
        'SH': {'DE': 'Schauer',
               'EN': 'Shower(s)',
               'FR': 'Averses'},
        'TS': {'DE': 'Gewitter',
               'EN': 'Thunderstorm',
               'FR': 'Orage'},
        'FZ': {'DE': 'gefrierend',
               'EN': 'freezing',
               'FR': 'surfondu'}
    }

    precipitation = \
    {
        'DZ': {'DE': 'Sprühregen',
               'EN': 'Drizzle',
               'FR': 'Bruine'},
        'RA': {'DE': 'Regen',
               'EN': 'Rain',
               'FR': 'Pluie'},
        'SN': {'DE': 'Schnee',
               'EN': 'Snow',
               'FR': 'Neige'},
        'SG': {'DE': 'Schneegriesel',
               'EN': 'Snow Grains',
               'FR': 'Neige en grains'},
        'IC': {'DE': 'Eisnadeln',
               'EN': 'Ice Crystals',
               'FR': 'Poudrin de glace'},
        'PL': {'DE': 'Eiskörper',
               'EN': 'Ice Pellets',
               'FR': 'Granules de glace'},
        'GR': {'DE': 'Hagel',
               'EN': 'Hail',
               'FR': 'Grêle'},
        'GS': {'DE': 'Reif/Frostgraupel',
               'EN': 'Small Hail and/or Snow Pellets',
               'FR': 'Grésil'},
        'UP': {'DE': 'Unbestimmter Niederschlag',
               'EN': 'Unknown Precipitation',
               'FR': 'averses inconnu'}
    }

    obscuration = \
    {
        'BR': {'DE': 'feuchter Dunst',
               'EN': 'Mist',
               'FR': 'Brume'},
        'FG': {'DE': 'Nebel',
               'EN': 'Fog',
               'FR': 'Brouillard'},
        'FU': {'DE': 'Rauch',
               'EN': 'Smoke',
               'FR': 'Fumée'},
        'VA': {'DE': 'Vulkanasche',
               'EN': 'Volcanic Ash',
               'FR': 'Cendres volcaniques'}, 	
        'DU': {'DE': 'verbreitet Staub',
               'EN': 'Widespread Dust',
               'FR': 'Poussière généralisée'}, 
        'SA': {'DE': 'Sand',
               'EN': 'Sand',
               'FR': 'Sable'},
        'HZ': {'DE': 'trockener Dunst',
               'EN': 'Haze',
               'FR': 'Brume sèche'}, 
        'PY': {'DE': 'Sprühnebel/Gischt',
               'EN': 'Spray',
               'FR': "Fumée d'eau"}
    }

    other = \
    {
        'PO': {'DE': 'Staub- und Sandwirbel',
               'EN': 'Well-Developed Dust/Sand Whirls',
               'FR': 'Tourbillons de sable'},
        'SQ': {'DE': 'Böen',
               'EN': 'Squalls',
               'FR': 'Grains'}, 	
        'FC': {'DE': 'Trombe / Windhose (mit Wasser: +FC)',
               'EN': 'Funnel Cloud Tornado Waterspout',
               'FR': 'Trombe terrestre ou marine'},
        'SS': {'DE': 'Sandsturm',
               'EN': 'Sandstorm',
               'FR': 'Tempête de sable'}, 
        'DS': {'DE': 'Staubsturm',
               'EN': 'Duststorm',
               'FR': 'Tempête de poussière'}
    }

        
    def __init__(self, url='http://weather.noaa.gov/pub/data/observations/metar/stations/'):
        Base.__init__(self, url)
        

        
        
        
if __name__ == "__main__":
    station =  raw_input('Station? > ').upper()

    taf = TAF()
    taf.download(station)
    
    metar = METAR()
    metar.download(station)

    print; print 'Encoded TAF info:'
    pprint(taf.get_encoded_info_dict())
    print; print 'Encoded TAF forecast:'
    pprint(taf.get_encoded_forecast_dict())
    print; raw_input('... give <RETURN> to exit')
