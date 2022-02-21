#!/usr/bin/env python3
"""
Simple script to print out the Danish holidays of a given year (first argument). 
If no argument is given, the current year is taken. 
"""
import sys
import datetime
import collections
from dateutil.easter import *
from dateutil.relativedelta import *

class DanishHolidays(object):

    def __init__(self, year):
        self.__year = year
        self.__holidays = {}
        self.__workdays = 0
        self.__weekends = 0

    @property
    def year(self):
        return self.__year
    
    def get_danish_holidays(self):
        eh = self.__get_easter_dependent_holidays()
        fh = self.__get_fixed_holidays()
        # Merge two Dictionaries
        holidays = {**eh, **fh}
        # Order it by Date, ascending
        sorted_dict = collections.OrderedDict(sorted(holidays.items(), key=lambda t: t[1]))
        # Aggregate stats
        for k,v in sorted_dict.items():
            if v.weekday() < 5: 
                self.__weekends += 1
            else: 
                self.__workdays += 1
        self.__holidays = sorted_dict
        return self.__holidays

    def __get_easter_dependent_holidays(self):
        # Dictionary of names of Holidays and their date relative to Easter.
        easter_date = easter(self.__year)
        relative_holidays = {
            "Fastelavn": -49,
            "Palmesøndag": -7,
            "Skærtorsdag": -3,
            "Langfredag": -2,
            "Påskedag": 0,
            "2. påskedag": 1,
            "Store Bededag": 26,
            "Kr. Himmelfart": 39,
            "Pinsedag": 49,
            "2. pinsedag": 50
        }
        result = {k : easter_date + relativedelta(days=+v) for (k,v) in relative_holidays.items()}
        return result

    def __get_fixed_holidays(self):
        # Dictionary of names of Holidays and their fixed date
        fixed_holidays = {
            "Juleaften": datetime.date(self.year, 12, 24),
            "1. juledag": datetime.date(self.year, 12, 25),
            "2. juledag": datetime.date(self.year, 12, 26),
            "Nytårsaften": datetime.date(self.year, 12, 31),
            "Nytårsdag": datetime.date(self.year, 1, 1),
            "Grundlovsdag": datetime.date(self.year, 6, 5),
        }        
        return fixed_holidays
    
    def get_danish_holidays_formatted(self, format='{:%d-%m-%Y}'):
        if not self.__holidays:
            self.get_danish_holidays()
        return {k:'{:%d-%m-%Y}'.format(v) for (k,v) in self.__holidays.items()}
        
    def get_danish_holidays_api(self):
        holidays = self.get_danish_holidays_formatted()
        stats = {"Hverdage" : self.__workdays, "Weekenddage" : self.__weekends}
        response = { "Stats" : stats, "Holidays" : holidays}
        return response
        
    def prettyprint(self):
        dict = self.get_danish_holidays_formatted()
        for k,v in dict.items():
            print(k, "\t", v)        
        print("\nHverdage: {0} \t Weekenddage: {1}".format(self.__workdays,self.__weekends))

def main(argv=None):
    if argv is None:
        argv = sys.argv
    year = datetime.date.today().year if len(argv) < 2 else int(argv[1])
    dh = DanishHolidays(year)
    dh.prettyprint()
    
if __name__ == '__main__':
    sys.exit(int(main() or 0))
