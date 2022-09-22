# Done by Bekzat Rakhimabyev 

import socket 
from sys import argv
import sys
import os
import time



def start(msg, address):
	print(f'session=\"{address[0]}:{address[1]}\" started')
	datas = msg.split(' | '.encode())
	userinfo['port'] = address[1]
	userinfo['size'] = int(datas[3].decode())
	userinfo['next_seq'] = int(datas[1].decode())+1
	userinfo['clienAddress'] = address
	userinfo['filename'] = datas[2].decode()
	userinfo['data'] = bytes()
	userinfo['lastUpdateTime'] = time.time()
	

def clearData():
	userinfo['port'] = 0
	userinfo['size'] = 1
	userinfo['next_seq'] = 0
	userinfo['clienAddress'] = (0, 0)
	userinfo['filename'] = None
	userinfo['data'] = bytes()
	userinfo['lastUpdateTime'] = time.time()


BUFFSIZE = 1024
port = int(argv[1:][0])
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('', port))
server.settimeout(3)
lastSeq = 1
userinfo = {}

try:
	while True:
		try:
			msg, clientAddress = server.recvfrom(BUFFSIZE)
			received = msg.split(' | '.encode())
			seq = int(received[1].decode())
			typ = received[0].decode()
			if typ == 's':
				start(msg, clientAddress)
				server.sendto(f'a | {seq + 1} | {BUFFSIZE}'.encode(), clientAddress)
			elif typ == 'd':
				if userinfo['next_seq'] == seq:
					userinfo['data'] += received[2]
					userinfo['next_seq'] = seq + 1 
					userinfo['lastUpdateTime'] = time.time
					server.sendto(f'a | {seq+1}'.encode(), clientAddress)
			if userinfo['filename'] == None:
				continue
			if userinfo['size'] == len(userinfo['data']):
				open(userinfo['filename'],'wb').write(userinfo['data'])
				print(f'session=\"{clientAddress[0]}:{clientAddress[1]}\" finished sucessfully')
				clearData()
				print(f'session=\"{clientAddress[0]}:{clientAddress[1]}\" removed after successful termination')
			if time.time() - userinfo['lastUpdateTime'] > 3:
				clearData()
				print(f'session=\"{clientAddress}\"  timeouted')
		except:
			pass
except KeyboardInterrupt:
	sys.exit() 


