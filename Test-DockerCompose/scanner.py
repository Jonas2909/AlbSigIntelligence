#!/bin/python3
import re
import os
import time
import schedule
import requests
import subprocess


def scan():

	# Get the current time as a struct_time object
	current_time_struct = time.localtime()

	# Format the date and time as minute-hour-day-month-year
	formatted_datetime = time.strftime("%M-%H-%d-%m-%Y", current_time_struct)

	output_file_name = formatted_datetime

	command = f"arp-scan -l > ./{output_file_name}.txt"

	process = subprocess.run(command, shell=True)

	# if ar-scan ran succefully do...
	if process.returncode == 0:	
		print("arp-scan ran successfully.")
	    
		url = 'https://0.0.0.0:5000/AddGraphData'
		
		mac_address_pattern = re.compile(r'(?:[0-9a-fA-F]:?){12}')
		
		mac_addresses = []

		try:
			file_path=f"{output_file_name}.txt"
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
		response = requests.post(url, json=data, verify=False)
		if response.status_code != 200:
			print(response)
			print(response.text)

	# if arp-scan failed...
	else:
	    print(f"arp-scan failed with return code {process.returncode}. Exiting.")


schedule.every().day.at("07:15").do(scan)
schedule.every().day.at("09:00").do(scan)
schedule.every().day.at("10:45").do(scan)
schedule.every().day.at("12:15").do(scan)
schedule.every().day.at("13:15").do(scan)
schedule.every().day.at("15:00").do(scan)
schedule.every().day.at("16:45").do(scan)
schedule.every().day.at("18:15").do(scan)

while True:
    schedule.run_pending()
    time.sleep(1)


