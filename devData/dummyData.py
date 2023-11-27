#!/bin/python3
from random import randrange

# init fixed data of scan
f_line = "Interface: <interFace>, type: EN10MB, MAC: <ma:cm:ac:ma:cm:ma>, IPv4: <141.87.XYZ.TUV>\n"
s_line = "Starting arp-scan 1.10.0 with 2048 hosts (https://github.com/royhills/arp-scan)\n"
ip_pre = "141.87."
ip_range_lowest = 56
ip_range_highest = 63
default = "(3c:0g:23:7d:13:d0)"
tab = "\t"
eof = "\n"

# get MACs
unknown = "(Unknown: locally administered)"
digits = "abcdef0123456789"
with open("vendors.txt") as f:
	content = f.readlines()


# output
data_out = open("dummyData.txt", "w")
data_out.write(f_line)
data_out.write(s_line)
for i in range(100):
	ip_range_1 = randrange(ip_range_lowest, ip_range_highest)
	ip_range_2 = randrange(253)
	ip_addr = ip_pre + str(ip_range_1) + "." + str(ip_range_2)
	mac = ""

	for n in range(6):
		idx = randrange(15)
		mac += digits[idx] + digits[(idx+5)//2] + ":"
	mac = mac[:-1]

	data_out.write(ip_addr + tab + mac + tab + default + tab + content[i])
