#!/bin/python3

import requests


url = 'http://0.0.0.0:5000/AddGraphData'
data =  {'time_stamp': '5','amount':'5'}
response = requests.post(url, data=data)
print(response)

