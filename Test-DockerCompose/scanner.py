#!/bin/python3
import re
import os
import time
import schedule
import requests
import subprocess
import hashlib


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
	    
		url = 'http://0.0.0.0:5000/AddGraphData'
		
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

		# delete first mac address which is MAC of scan header in .txt file
		mac_addresses=mac_addresses[1:]
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

		# send MAC Hashes and timestamp
		for MAC in mac_addresses:
			hashed_mac_address = hashlib.sha256(MAC.encode()).hexdigest()
			data={ 'hashed_mac_address': hashed_mac_address, 'time_stamp': current_unix_time,}
			response = requests.post(url, json=data)

		# Delete the file after processing and sending data
		try:
			os.remove(file_path)
			print(f"File '{file_path}' deleted successfully.")
		except FileNotFoundError:
			print(f"Error: File '{file_path}' not found.")
		except Exception as e:
			print(f"Error deleting file '{file_path}': {e}")

	# if arp-scan failed...
	else:
	    print(f"arp-scan failed with return code {process.returncode}. Exiting.")

# Time is UTC, needs to be changed to UTC+1
schedule.every().day.at("08:15").do(scan)
schedule.every().day.at("10:00").do(scan)
schedule.every().day.at("11:45").do(scan)
schedule.every().day.at("13:15").do(scan)
schedule.every().day.at("14:15").do(scan)
schedule.every().day.at("16:00").do(scan)
schedule.every().day.at("17:45").do(scan)
schedule.every().day.at("19:15").do(scan)

# scheduled task for development
schedule.every().day.at("16:31").do(scan)


while True:
    schedule.run_pending()
    time.sleep(1)


