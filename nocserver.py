#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aiohttp import web
import socketio
from os import system
import random
import json

# creates a new Async Socket IO Server
sio = socketio.AsyncServer()
# Creates a new Aiohttp Web Application
app = web.Application()
# Binds our Socket.IO server to our Web App
# instance
sio.attach(app)

# Just for debug
@sio.on('connect')
def connect(sid, environ):
	print("connect ", sid)

# Just for debug
@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

def generate_test_ring(fname, xsz):
	file = open(fname+".txt", "w")
	xsz = int(xsz)
	for i in range(0, random.randint(2,50)):
		file.write(str(random.randint(0, xsz-1))+"\t")
		file.write(str(random.randint(0, xsz-1))+"\t")
		file.write("\"")
		for j in range(0, random.randint(5,15)):
			file.write(chr(random.randint(65, 122)))
		file.write("\"\t")
		file.write(str(random.randint(0,255)))
		file.write("\n")
	file.close()
	system("./espserver.py ring "+fname+".txt")

def generate_test_mesh(fname, xsz, ysz):
	file = open(fname+".txt", "w")
	xsz = int(xsz)
	ysz = int(ysz)
	for i in range(1, random.randint(2,50)):
		file.write(str(random.randint(0, xsz-1))+str(random.randint(0, ysz-1))+"\t")
		file.write(str(random.randint(0, xsz-1))+str(random.randint(0, ysz-1))+"\t")
		file.write("\"")
		for j in range(0, random.randint(5,15)):
			file.write(chr(random.randint(65, 122)))
		file.write("\"\t")
		file.write(str(random.randint(0,255)))
		file.write("\n")
	file.close()
	system("./espserver.py mesh "+fname+".txt")

@sio.on('simulate')
async def print_message(sid, data):
	print("Socket ID: " , sid)
	if data["topology"]=="Mesh":
		generate_test_mesh(sid, data["xsize"], data["ysize"])
		system("./nocemu json "+data["topology"].lower()+" "+str(data["xsize"])+" "+str(data["ysize"])+" "+str(sid)+".txt")
	else:
		generate_test_ring(sid, data["xsize"])
		system("./nocemu json "+data["topology"].lower()+" "+str(data["xsize"])+" "+str(sid)+".txt")
	
	jsfile = open(sid+".json")
	out_data = json.load(jsfile)
	await sio.emit('result', out_data)
	jsfile.close()

if __name__ == '__main__':
    web.run_app(app)