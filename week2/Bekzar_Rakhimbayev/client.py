
import socket 
from sys import argv

def Main():
	host, port = argv[1].split(':')
	port = int(port)
	numbers = [15492781, 15492787, 15492803, 15492811, 15492810, 15492833, 15492859, 15502547, 15520301, 15527509, 15522343, 1550784]

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	client.connect((host, port))
	for i in numbers:
		client.send(str(i).encode())
		data = client.recv(1024)
		print(f'Recieved message: {data.decode()}')
	client.close()

if __name__ == '__main__':
	try:
		Main()
	except:
		print('terminated')