#!/bin/sh

# init file and perform arp-scan
filename="$(date +%d_%m_%y_)ScanResults.txt"
echo "\nScanning ..."
arp-scan -l > "$filename" 
echo "Done\n"

# init Data for Request and Print results
amount=$(cat "$filename" | egrep ^192 | egrep -v "Cisco" | egrep -v "Link" | wc -l)
timeday=$(date +%s)
echo "Results, counted: $amount, at $timeday ..."

# build and send Request
curl -X POST http://0.0.0.0:5000/AddGraphData -H "Content-Type: application/json" -d '{"quantity": '"$amount"', "time_stamp": '"$timeday"'}'

# delete save file
rm "$filename"
echo "\nFinished\n================="

