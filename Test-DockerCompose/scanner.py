#!/bin/python3
import re
import os
import time
import schedule
import requests
import subprocess

def scan():
	batcmd= "./automationArp"
    	result = subprocess.check_output(batcmd, shell=True, text=True)
	return


schedule.every().day.at("08:15").do(scan)
schedule.every().day.at("10:00").do(scan)
schedule.every().day.at("11:45").do(scan)
schedule.every().day.at("13:15").do(scan)
schedule.every().day.at("14:15").do(scan)
schedule.every().day.at("16:00").do(scan)
schedule.every().day.at("17:45").do(scan)
schedule.every().day.at("19:15").do(scan)

while True:
    schedule.run_pending()
    time.sleep(1)


