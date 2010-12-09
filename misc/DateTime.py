# -*- coding: iso-8859-1 -*-

#===============================================================================
# Commons DateTime module.
# by Mark Muzenhardt, published under GPL-License.
#===============================================================================

import time


class Calendar:
    day_names_dict = \
        {
        'DE': {
            1: 'Montag',
            2: 'Dienstag',
            3: 'Mittwoch',
            4: 'Donnerstag',
            5: 'Freitag',
            6: 'Samstag',
            7: 'Sonntag'},
        'EN': {
            1: 'Monday',
            2: 'Tuesday',
            3: 'Wednesday',
            4: 'Thursday',
            5: 'Friday',
            6: 'Saturday',
            7: 'Sunday'}
        }

    month_names_dict = \
        {
        'DE': {
             1: 'Januar',
             2: 'Februar',
             3: 'März',
             4: 'April',
             5: 'Mai',
             6: 'Juni',
             7: 'Juli',
             8: 'August',
             9: 'September',
            10: 'Oktober',
            11: 'November',
            12: 'Dezember'},
        'EN': {
             1: 'January',
             2: 'February',
             3: 'March',
             4: 'April',
             5: 'Mai',
             6: 'June',
             7: 'July',
             8: 'August',
             9: 'September',
            10: 'October',
            11: 'November',
            12: 'December'}
        }

    def __init__(self, language='DE'):
        self.language = language



class DateTime:
    ''' Datetime functions. '''

    def __init__(self):
        self.Date = Date()
        self.Time = Time()


    def set(self, year=0, month=0, day=0, hour=0, minute=0, second=0):
        ''' Basic datetime setting. '''

        self.Date.set(year, month, day)
        self.Time.set(hour, minute, second)
        return


    def set_from_local(self, timezone):
        ''' Set from local computer time. '''

        now = time.localtime()
        year = now.tm_year
        month = now.tm_mon
        day = now.tm_mday
        self.Date.set(year, month, day)

        hour = now.tm_hour
        minute = now.tm_min
        second = now.tm_sec
        self.Time.set(hour, minute, second)
        return


    def set_from_str(self, datetime_str, datetime_format='DD.MM.YYYY hh:mm:ss'):
        ''' Set from a string with given format. '''

        format_list = datetime_format.split(' ')
        date_format = format_list[0]
        time_format = format_list[1]

        datetime_list = datetime_str.split(' ')
        date_str = datetime_list[0]
        time_str = datetime_list[1]

        self.Date.set_from_str(date_str, date_format)
        self.Time.set_from_str(time_str, time_format)
        return


    def get(self):
        ''' Returns date as a set of three variables. '''

        year, month, day = self.Date.get()
        hour, minute, second = self.Time.get()
        return year, month, day, hour, minute, second


    def get_str(self, datetime_format='DD.MM.YYYY hh:mm:ss'):
        ''' Returns date as string in given format. '''

        format_list = datetime_format.split(' ')
        date_format = format_list[0]
        time_format = format_list[1]

        date_str = self.Date.get_str(date_format)
        time_str = self.Time.get_str(time_format)

        datetime_str = '%s %s' % (date_str, time_str)
        return datetime_str



class Date:
    def set(self, year=0, month=0, day=0):
        ''' Basic date setting from three variables. '''

        self.year = year
        self.month = month
        self.day = day
        return


    def set_from_local(self):
        ''' Set date from local computer time. '''

        now = time.localtime()
        self.year = now.tm_year
        self.month = now.tm_mon
        self.day = now.tm_mday
        return


    def set_from_str(self, date_str, date_format='DD.MM.YYYY'):
        ''' Set date from a string with given format. '''

        day_left = date_format.find('D')
        day_right = date_format.rfind('D') + 1
        month_left = date_format.find('M')
        month_right = date_format.rfind('M') + 1
        year_left = date_format.find('Y')
        year_right = date_format.rfind('Y') + 1

        self.year = int(date_str[year_left:year_right])
        self.month = int(date_str[month_left:month_right])
        self.day = int(date_str[day_left:day_right])
        return


    def get(self):
        ''' Returns date as a set of three variables. '''
        return self.year, self.month, self.day


    def get_str(self, date_format='DD.MM.YYYY'):
        ''' Returns date as string in given format. '''

        dict = {'year': self.year, 'month': self.month, 'day': self.day}

        date_str = date_format
        date_str = date_str.replace('YYYY', '%(year)04i')
        date_str = date_str.replace('YY'  , '%(year)02i')
        date_str = date_str.replace('MM'  , '%(month)02i')
        date_str = date_str.replace('DD'  , '%(day)02i')
        date_str = date_str % dict
        return date_str



class Time:
    def set(self, hour=0, minute=0, second=0):
        ''' Basic date setting from three variables. '''

        self.hour = hour
        self.minute = minute
        self.second = second
        return


    def set_from_local(self):
        ''' Set time from local computer time. '''

        now = time.localtime()
        self.hour = now.tm_hour
        self.minute = now.tm_min
        self.second = now.tm_sec
        return


    def set_from_str(self, time_str, time_format='hh:mm:ss'):
        ''' Set time from a string with given format. '''

        hour_left = time_format.find('h')
        hour_right = time_format.rfind('h') + 1
        minute_left = time_format.find('m')
        minute_right = time_format.rfind('m') + 1
        second_left = time_format.find('s')
        second_right = time_format.rfind('s') + 1

        self.hour = int(time_str[hour_left:hour_right])
        self.minute = int(time_str[minute_left:minute_right])
        self.second = int(time_str[second_left:second_right])
        return


    def get(self):
        ''' Returns time as a set of three variables. '''
        return self.hour, self.minute, self.second


    def get_str(self, time_format='hh:mm:ss'):
        ''' Returns time as string in given format. '''

        dict = {'hour': self.hour, 'minute': self.minute, 'second': self.second}

        time_str = time_format
        time_str = time_str.replace('hh', '%(hour)02i')
        time_str = time_str.replace('mm', '%(minute)02i')
        time_str = time_str.replace('ss', '%(second)02i')
        time_str = time_str % dict
        return time_str


