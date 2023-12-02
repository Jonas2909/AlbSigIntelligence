#!/bin/python3
from datetime import datetime
import requests

year = 2023
month = 11
days = [] # 01.11.2023 = Mittwoch
for day in range(1,31):
    if day in [4,5,11,12,18,19,25,26]:
        continue
    else:
        days.append(day)
hours = [8, 10, 11, 14, 15, 16, 17]
minutes = [15, 0, 45, 15, 15, 0, 45]

# create unix timestamps
time_stamps = []
for d in days:
    for i, h in enumerate(hours):
        unix_timestamp = (datetime(year, month, d, h, minutes[i]) - datetime(1970, 1, 1)).total_seconds()
        time_stamps.append(int(unix_timestamp))

# send request
    
"""
url = 'http://0.0.0.0:5000/AddGraphData'
data =  {'time_stamp': 5,'quantity':5}
response = requests.post(url, json=data)
print(response.text)
"""
