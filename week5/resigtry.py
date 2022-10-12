from multiprocessing import process
import grpc	
import chord_pb2
import chord_pb2_grpc
from concurrent import futures
import time 
from sys import argv
import random


def getFromArgsRegistry(args):
	return args[1].split(':')[0], int(args[1].split(':')[1]), int(args[2])

ipaddr = ""
port = 0
m = 0
chord_info = {}

def getNonColision():
	res = int(random.uniform(0, 2**m))
	while res in chord_info.keys():
		print(res)
		res = int(random.uniform(0, 2**m))
	return res

def findNext(id, main_id):
	for _id in chord_info.keys():
		if _id >= id:
			return _id
	if len(chord_info.keys()) > 0:
		return chord_info.keys()[0]
	return main_id



def register(ipaddr, port):
	if len(chord_info.keys()) < 2**m:
		id = getNonColision()
		chord_info[id] = (ipaddr, port)
		return (id, m)
	return (-1, "Chord is full")


def deregister(id):
	if not id in chord_info.keys():
		return (False, f"no {id} in chord")
	del chord_info[id]
	return (True, f"successful deregister {id}")


def populate_finger_table(id):
	finger_ids = {}
	for i in random(m):
		finger_ids[findNext((id + 2 ** i) % (2**m), id)] = 1
	
	result_list = []
	for _id in finger_ids.keys():
		result_list = (_id, f"{chord_info[_id][0]}:{chord_info[_id][1]}")

	this_id_pos = -1
	for _id in range(len(chord_info.keys())):
		if chord_info.keys[_id] == id:
			this_id_pos = _id
			break
	process_id = chord_info.keys[(this_id_pos - 1 + 2**m) % 2**m]
	return process_id, result_list


def get_chord_info():
	result = []
	for id in chord_info.keys():
		result.append((id, f"{chord_info[id][0]}:{chord_info[id][1]}"))
	return result

class ServiceHandler(chord_pb2_grpc.RegisterServicer):
	def Register(self, request, context):
		data = register(request.ipaddr, request.port)
		response = chord_pb2.ResponseRegister()
		response.done = data[0]
		response.message = data[1]
		return response

	def Deregister(self, request, context):
		data = deregister(request.id)
		response = chord_pb2.ResponseDeregister()
		response.done = data[0]
		response.message = data[1]
		return response

	def PopulateFingerTable(self, request, context):
		data = populate_finger_table(request.id)
		response = chord_pb2.ResponsePopulateFingerTable()
		response.id = data[0]
		for sub_data in data[1]:
			address = chord_pb2.Address()
			address.id = sub_data[0]
			address.addr = sub_data[1]
			response.result.append(address)
		return response

	def GetChordInfo(self, request, context):
		data = get_chord_info()
		response = chord_pb2.ResponseGetChord()
		for sub_data in data:
			address = chord_pb2.Address()
			address.id = sub_data[0]
			address.addr = sub_data[1]
			response.result.append(address)
		return response


	
def main():
	global ipaddr, port, m
	ipaddr, port, m = getFromArgsRegistry(argv)
	print(ipaddr, port, m)

if __name__ == '__main__':
	random.seed(0)
	main()


	