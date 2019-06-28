#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import socket
import sys

# HOST = ''	# Symbolic name, meaning all available interfaces
# PORT = 8888	# Arbitrary non-privileged port


socket.setdefaulttimeout(5)

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('10.42.0.1', 8888 ))
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
	data = line.split('\t')
	client.send(data[0])
	client.send(data[1])

f.close()

print("Closing connection")
client.close()