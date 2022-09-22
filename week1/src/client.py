# Done by Bekzat Rakhimabyev 

import socket	
from sys import argv
import sys
import time

def connecting(address):
	for tries in range(5):
		client.sendto(f's | 0 | {name2} | {len(data)}'.encode(), address)
		msg = client.recvfrom(BUFFSIZE)[0].decode('utf-8')
		global size 
		msg = msg.split('|')
		size = int(msg[2])
		if msg[0][0] == 'a':
			return True
	return False

def splitting(data):
	ans = []
	pos = 0
	while pos < len(data):
		piece = f'd | {len(ans)+1} | '.encode()
		ans.append(data[pos:min(len(data), pos+size-len(piece))])
		pos += size-len(piece)
	return ans

BUFFSIZE=2048
host, name1, name2 = argv[1:]
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(0.5)
addr,port = host.split(':')
port = int(port)
address = (addr, port) 
client.bind(('', 0))
data = open(name1, 'rb').read()

if connecting(address) == False:
	client.close()
	exit()
seqno = 1
pieces = splitting(data)
for piece in pieces:
	sended = False
	for tries in range(5):
		client.sendto(f'd | {seqno} | '.encode()+piece, address)
		try: 
			msg = client.recvfrom(BUFFSIZE)[0].decode('utf-8')
			msg = msg.split('|')
			if msg[0][0] == 'a' and seqno < int(msg[1]):
				seqno = max(seqno, int(msg[1]))
				sended = True
				break
		except :
			pass

	if sended == False:
		client.close()
		sys.exit()
client.close()
