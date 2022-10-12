from platform import node
import grpc  
import chord_pb2
import chord_pb2_grpc
from concurrent import futures
import time 
from sys import argv, exit
import random
import zlib


def getFromArgsNode(args):
	return args[1].split(':')[0], int(args[1].split(':')[1]), args[2].split(':')[0], int(args[2].split(':')[1]),


ipaddr = ""
port = 0
registry_ipaddr = ""
registry_port = 0

m = 0
finger_table = {}
process_id = 0
self_id = 0


node_data = {}

def processUpdate(new_process_id):
	if(new_process_id > process_id):
		for key in node_data:
			hash_value = zlib.adler32(key.encode())
			target_id = hash_value % 2 ** m
			if isGoodId(target_id, process_id, new_process_id):
				try:
					with grpc.insecure_channel(f'{finger_table.keys[0][0]}:{finger_table.keys[0][1]}') as channel:
						stub = chord_pb2_grpc.NodeStub(channel)
						stub.SaveData(chord_pb2.RequestSave(key=key, text=node_data[key]))
				except ValueError:
					pass

def set_finger_table(given_finger_table):
	finger_table.clear()
	for data in given_finger_table:
		finger_table[data[0]] = (data[1].split(':')[0], int(data[1].split(':')[1]))

def get_finger_table():
	result = []
	for id in finger_table.keys():
		result.append((id, f"{finger_table[id][0]}:{finger_table[id][1]}"))
	return result

def isGoodId(id, process_id, self_id):
	if process_id > self_id:
		return id in [x for x in range(2**m) if x > process_id or x <= self_id]
	return id in [x for x in range(2**m) if x > process_id and x <= self_id]

def isGoodId(id):
	if process_id > self_id:
		return id in [x for x in range(2**m) if x > process_id or x <= self_id]
	return id in [x for x in range(2**m) if x > process_id and x <= self_id]

def save(key, text):
	hash_value = zlib.adler32(key.encode())
	target_id = hash_value % 2 ** m
	if isGoodId(target_id, process_id, self_id):
		node_data[key] = text
		return (True, self_id)
	elif isGoodId(target_id, self_id, finger_table.keys[0]):
		try:
			with grpc.insecure_channel(f'{finger_table.keys[0][0]}:{finger_table.keys[0][1]}') as channel:
				stub = chord_pb2_grpc.NodeStub(channel)
				response = stub.SaveData(chord_pb2.RequestSave(key=key, text=text))
				return (response.ok, response.message)
		except ValueError:
			return (False, f"can not connect to node {finger_table.keys[0][0]}:{finger_table.keys[0][1]}")
	else:
		for i in len(finger_table.keys()):
			id1 = finger_table.keys[i]
			id2 = finger_table.keys[(i + 1)%len(finger_table.keys())]
			if isGoodId(key, id1, id2):
				try:
					with grpc.insecure_channel(f'{finger_table.keys[id1][0]}:{finger_table.keys[id1][1]}') as channel:
						stub = chord_pb2_grpc.NodeStub(channel)
						response = stub.SaveData(chord_pb2.RequestSave(key=key, text=text))
						return (response.ok, response.message)
				except ValueError:
					return (False, f"can not connect to node {finger_table.keys[id1][0]}:{finger_table.keys[id1][1]}")


def remove(key):
	hash_value = zlib.adler32(key.encode())
	target_id = hash_value % 2 ** m
	if isGoodId(target_id, process_id, self_id):
		if key in node_data:
			return (True, self_id)
		else:
			return (False, "no data in this key to delete")
	elif isGoodId(target_id, self_id, finger_table.keys[0]):
		try:
			with grpc.insecure_channel(f'{finger_table.keys[0][0]}:{finger_table.keys[0][1]}') as channel:
				stub = chord_pb2_grpc.NodeStub(channel)
				response = stub.Remove(chord_pb2.RequestRemove(key=key))
				return (response.ok, response.message)
		except ValueError:
			return (False, f"can not connect to node {finger_table.keys[0][0]}:{finger_table.keys[0][1]}")
	else:
		for i in len(finger_table.keys()):
			id1 = finger_table.keys[i]
			id2 = finger_table.keys[(i + 1)%len(finger_table.keys())]
			if isGoodId(key, id1, id2):
				try:
					with grpc.insecure_channel(f'{finger_table.keys[id1][0]}:{finger_table.keys[id1][1]}') as channel:
						stub = chord_pb2_grpc.NodeStub(channel)
						response = stub.Remove(chord_pb2.RequestRemove(key=key))
						return (response.ok, response.message)
				except ValueError:
					return (False, f"can not connect to node {finger_table.keys[id1][0]}:{finger_table.keys[id1][1]}")

def find(key):
	hash_value = zlib.adler32(key.encode())
	target_id = hash_value % 2 ** m
	if isGoodId(target_id, process_id, self_id):
		if key in node_data:
			return (True, self_id, f"{ipaddr}:{port}")
		else:
			return (False, "no data in this key")
	elif isGoodId(target_id, self_id, finger_table.keys[0]):
		try:
			with grpc.insecure_channel(f'{finger_table.keys[0][0]}:{finger_table.keys[0][1]}') as channel:
				stub = chord_pb2_grpc.NodeStub(channel)
				response = stub.Find(chord_pb2.RequestRemove(key=key))
				return (response.ok, response.message)
		except ValueError:
			return (False, f"can not connect to node {finger_table.keys[0][0]}:{finger_table.keys[0][1]}")
	else:
		for i in len(finger_table.keys()):
			id1 = finger_table.keys[i]
			id2 = finger_table.keys[(i + 1)%len(finger_table.keys())]
			if isGoodId(key, id1, id2):
				try:
					with grpc.insecure_channel(f'{finger_table.keys[id1][0]}:{finger_table.keys[id1][1]}') as channel:
						stub = chord_pb2_grpc.NodeStub(channel)
						response = stub.Find(chord_pb2.RequestRemove(key=key))
						return (response.ok, response.message)
				except ValueError:
					return (False, f"can not connect to node {finger_table.keys[id1][0]}:{finger_table.keys[id1][1]}")

def quit():
	try:
		with grpc.insecure_channel(f'{registry_ipaddr}:{registry_port}') as channel:
			stub = chord_pb2_grpc.RegisterStub(channel)
			stub.Deregister(chord_pb2.RequestDeregister(id=self_id))
	except ValueError:
		pass
	time.sleep(1)
	for key in node_data:
		try:
			with grpc.insecure_channel(f'{finger_table.keys[0][0]}:{finger_table.keys[0][1]}') as channel:
				stub = chord_pb2_grpc.NodeStub(channel)
				stub.SaveData(chord_pb2.RequestSave(key=key, text=node_data[key]))
		except ValueError:
			pass
	exit(0)


class ServiceHandler(chord_pb2_grpc.Node):
	def GetFinger_table(self, request, context):
		data = get_finger_table()
		response = chord_pb2.ResponseFingerTable()
		for sub_data in data:
			address = chord_pb2.Address()
			address.id = sub_data[0]
			address.addr = sub_data[1]
			response.result.append(address)
		return response

	def SaveData(self, request, context):
		data = save(request.key, request.text)
		response = chord_pb2.ResponseAction()
		response.ok	= data[0]
		response.message = data[1]
		return response

	def Remove(self, request, context):
		data = remove(request.key)
		response = chord_pb2.ResponseAction()
		response.ok	= data[0]
		response.message = data[1]
		return response

	def Find(self, request, context):
		data = find(request.key)
		response = chord_pb2.ResponseAction()
		response.ok	= data[0]
		response.message = data[1]
		return response


def main():
	global registry_ipaddr, registry_port, ipaddr, port
	registry_ipaddr, registry_port, ipaddr, port = getFromArgsNode(argv)
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
	chord_pb2_grpc.add_NodeServicer_to_server(ServiceHandler(), server)
	server.add_insecure_port(f'{ipaddr}:{port}')
	server.start()
	try:
		server.wait_for_termination()
	except KeyboardInterrupt:
		print("Shutting down")

if __name__ == '__main__':
	main()