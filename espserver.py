#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys

socket.setdefaulttimeout(5)

s = socket.socket()
s.bind(('0.0.0.0', 8090 ))
s.listen(0)

# Blocking:
try:
	print("Awaiting client connection...")
	client, addr = s.accept()
except:
	print("Failed to connect to ESP32")
	exit(0)

# Send if ring or mesh
client.send(sys.argv[1])

# Retrieve data from sys.argv[2]
f = open(sys.argv[2], 'r')

for line in f:
	data = line.split(' ')
	client.send(data[0])
	client.send(data[1])

f.close()

print("Closing connection")
client.close()