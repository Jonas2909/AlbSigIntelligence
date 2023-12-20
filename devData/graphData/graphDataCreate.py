#!/bin/python3
from datetime import datetime
import requests
import random

url = 'http://0.0.0.0:5000/AddGraphData'

year = 2023
month = 12
days = [] 
# 01.11.2023 = Mittwoch
for day in range(1,31):
    if day in [4,5,11,12,18,19,25,26]:
        continue
    else:
        days.append(day)
# simulate scan 15min after start of lecture
hours = [8, 10, 11, 14, 15, 16, 17]
minutes = [15, 0, 45, 15, 15, 0, 45]

# create unix timestamps for all hours
time_stamps = []
for d in days:
    for i, h in enumerate(hours):
        unix_timestamp = (datetime(year, month, d, h, minutes[i]) - datetime(1970, 1, 1)).total_seconds()
        time_stamps.append(unix_timestamp)

# send requests
for t in time_stamps:
    amount = random.randint(45, 90)
    data =  { 'time_stamp': t,'quantity': amount }
    response = requests.post(url, json=data)
    if response.status_code != 200:
        print(response)
        print(response.text)
