#!/bin/python3
import re
import time
import requests

url = 'http://0.0.0.0:5000/AddGraphData'

mac_address_pattern = re.compile(r'(?:[0-9a-fA-F]:?){12}')

mac_addresses = []

try:
	file_path="arp_scan_output.txt"
	
	with open(file_path, 'r') as file:
        	for line in file:
            		line = line.strip()
            		matches = mac_address_pattern.findall(line)
            		mac_addresses.extend(matches)        
        
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")

# get amount of unique MACs
amount = len(mac_addresses)

# get current time
current_unix_time = int(time.time())
    
data={ 'time_stamp': current_unix_time,'quantity': amount}        

# send timestamp with amount


response = requests.post(url, json=data)
if response.status_code != 200:
	print(response)
	print(response.text)




