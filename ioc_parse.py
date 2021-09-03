#!/usr/bin/env python3

import requests
from datetime import datetime


# Returns the number of days between day_one and day_two.
def days_delta(day_one, day_two):
    day_one = datetime.strptime(day_one, "%Y-%m-%d")
    day_two = datetime.strptime(day_two, "%Y-%m-%d")
    return abs((day_one - day_two).days)


# Returns a dictionary where the IP address is the key and the entire list (each line in the CSV from the site) is the value.
def generate_ioc_dict():
    data = requests.get('https://feodotracker.abuse.ch/downloads/ipblocklist.csv').text.splitlines()
    indicator_list = [line.strip("\"") for line in data if "#" not in line if "first_seen_utc" not in line]
    ioc_dict = {}
    for ioc in indicator_list:
        ioc_list = ioc.replace(" ", ",").split(",")
        ioc_dict[ioc_list[2]] = ioc_list
    return(ioc_dict)
    
    
def main():
    todays_date = datetime.now().strftime('%Y-%m-%d')
    ioc_dict = generate_ioc_dict()
    for k, v in ioc_dict.items():
        days_between = days_delta(todays_date, v[0])  # Calculates how may days are between today and the first time the IOC was seen.
        if days_between == 0:
            print("%s IP address %s was first seen today." % (v[-1], v[2]))
        else:
            print("%s IP address %s was first seen %s day(s) ago." %
                  (v[-1], v[2], days_between))
                  
                  
if __name__ == '__main__':
    main()
