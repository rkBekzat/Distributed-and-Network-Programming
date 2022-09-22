from _thread import * 
import threading
import time  
import socket 
from sys import argv
import multiprocessing  

lock = threading.Lock()
WORKERCOUNT = 3
threadWorking = True

queue = multiprocessing.Queue()

def isprime(n):
	if n in (2, 3):
		return True
	if n % 2 == 0:
		return False
	for div in range(3, n, 2):
		if n % div == 0:
			return False 
	return True

def worker():
	while threadWorking:
		try:
			if queue.empty():
				time.sleep(0.1)
				continue
			conn, addr = queue.get()
			print(f'{addr} connected')
			while threadWorking:
				try:
					msg = conn.recv(1024).decode()
					if not msg: 
						conn.close()
						print(f'{addr} disconnected')
						break
					if isprime(int(msg)) == True:
						conn.send(f'{msg} is prime'.encode())
					else:
						conn.send(f'{msg} is not prime'.encode())
				except:
					break
		except:
			pass 
		


port = int(argv[1]) 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', port))
server.listen()
threads = [threading.Thread(target=worker, args=()) for i in range(WORKERCOUNT)]
for t in threads:
	t.start()

try:
	while threadWorking:
		conn, addr = server.accept() 
		queue.put((conn, addr))
except KeyboardInterrupt:
	print('Shutting down')
	threadWorking = False
	for t in threads:
		t.join() 
	print('Done')

