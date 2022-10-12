import grpc  
# import service_pb2
# import service_pb2_grpc
from concurrent import futures
import time 
from sys import argv
import random


def getFromArgsNode(args):
	return args[1].split(':')[0], int(args[1].split(':')[1]), args[2].split(':')[0], int(args[2].split(':')[1]),


ipaddr = ""
port = 0
registry_ipaddr = ""
registry_port = 0

m = 0
finger_table = {}


def set_finger_table(given_finger_table):
	finger_table.clear()
	for data in given_finger_table:
		finger_table[data[0]] = (data[1].split(':')[0], int(data[1].split(':')[1]))

def get_finger_table():
	result = []
	for id in finger_table.keys():
		result.append((id, f"{finger_table[id][0]}:{finger_table[id][1]}"))
	return result

def save(key, text):
	pass 

def remove(key):
	pass 

def find(key):
	pass 


def main():
	global registry_ipaddr, registry_port, ipaddr, port
	registry_ipaddr, registry_port, ipaddr, port = getFromArgsNode(args)

if __name__ == '__main__':
	main()