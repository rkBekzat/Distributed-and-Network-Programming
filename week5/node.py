from _thread import *
import threading
import time
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
	global process_id
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
	process_id = new_process_id

def set_finger_table(given_finger_table):
	finger_table.clear()
	for data in given_finger_table:
		finger_table[data[0]] = (data[1].split(':')[0], int(data[1].split(':')[1]))
	# print(finger_table)

def get_finger_table():
	result = []
	for id in finger_table.keys():
		result.append((id, f"{finger_table[id][0]}:{finger_table[id][1]}"))
	return result

def isGoodId(id, process_id, self_id):
	if process_id > self_id:
		return (id > process_id or id <= self_id)
	return (id > process_id and id <= self_id)


def findNext(id, main_id):
	list_id = sorted(finger_table.keys())
	for _id in list_id:
		if _id >= id % 2**m:
			return _id
	if len(list_id) > 0:
		return sorted(list_id)[0]
	return main_id

def save(key, text):
	hash_value = zlib.adler32(key.encode())
	target_id = hash_value % 2 ** m
	print('Target:', target_id)
	print('PRoc id ', process_id)
	print('Selfid:', self_id)

	list_ids = sorted(finger_table.keys())
	next_id = findNext(self_id)

	if isGoodId(target_id, process_id, self_id):
		node_data[key] = text
		return (True, self_id)
	elif isGoodId(target_id, self_id, next_id):
		print("Second state")
		try:
			print("Tried to connect")
			print(next_id)
			print(finger_table[next_id])
			print(finger_table.keys())
			print(finger_table[next_id][0])
			with grpc.insecure_channel(f'{finger_table[next_id][0]}:{finger_table[next_id][1]}') as channel:
				stub = chord_pb2_grpc.NodeStub(channel)
				response = stub.SaveData(chord_pb2.RequestSave(key=key, text=text))
				return (response.ok, response.message)
		except ValueError:
			return (False, f"can not connect to node {finger_table[next_id][0]}:{finger_table[next_id][1]}")
	else:
		print(list_ids)
		for i in range(len(list_ids)):
			id1 = list_ids[i]
			id2 = list_ids[(i + 1)%len(list_ids)]
			if isGoodId(target_id, id1, id2):
				try:
					with grpc.insecure_channel(f'{finger_table[id1][0]}:{finger_table[id1][1]}') as channel:
						stub = chord_pb2_grpc.NodeStub(channel)
						response = stub.SaveData(chord_pb2.RequestSave(key=key, text=text))
						return (response.ok, response.message)
				except ValueError:
					return (False, f"can not connect to node {finger_table[id1][0]}:{finger_table[id1][1]}")

def remove(key):
	hash_value = zlib.adler32(key.encode())
	target_id = hash_value % 2 ** m
	if isGoodId(target_id, process_id, self_id):
		print("TEST THIS BECKA")
		if key in node_data:
			return (True, self_id)
		else:
			return (False, "no data in this key to delete")
	elif isGoodId(target_id, self_id, finger_table.keys[0]):
		print("TEST THIS BECKA")
		try:
			with grpc.insecure_channel(f'{finger_table.keys[0][0]}:{finger_table.keys[0][1]}') as channel:
				stub = chord_pb2_grpc.NodeStub(channel)
				response = stub.Remove(chord_pb2.RequestRemove(key=key))
				return (response.ok, response.message)
		except ValueError:
			return (False, f"can not connect to node {finger_table.keys[0][0]}:{finger_table.keys[0][1]}")
	else:
		print("TEST THIS BECKA")
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
		print("TEST THIS BECKA")
		if key in node_data:
			return (True, self_id, f"{ipaddr}:{port}")
		else:
			return (False, "no data in this key")
	elif isGoodId(target_id, self_id, finger_table.keys[0]):
		print("TEST THIS BECKA")
		try:
			with grpc.insecure_channel(f'{finger_table.keys[0][0]}:{finger_table.keys[0][1]}') as channel:
				stub = chord_pb2_grpc.NodeStub(channel)
				response = stub.Find(chord_pb2.RequestRemove(key=key))
				return (response.ok, response.message)
		except ValueError:
			return (False, f"can not connect to node {finger_table.keys[0][0]}:{finger_table.keys[0][1]}")
	else:
		print("TEST THIS BECKA")
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
			stub = chord_pb2_grpc.RegistryStub(channel)
			res = stub.Deregister(chord_pb2.RequestDeregister(id=self_id))
			print(res.message)
			if not res.done:
				return
	except ValueError:
		pass
	time.sleep(1)
	for key in node_data:
		print("TEST THIS BECKA")
		try:
			with grpc.insecure_channel(f'{finger_table.keys[0][0]}:{finger_table.keys[0][1]}') as channel:
				stub = chord_pb2_grpc.NodeStub(channel)
				stub.SaveData(chord_pb2.RequestSave(key=key, text=node_data[key]))
		except ValueError:
			pass
	exit(0)


class ServiceHandler(chord_pb2_grpc.Node):
	def GetFingerTable(self, request, context):
		data = get_finger_table()
		response = chord_pb2.ResponseFingerTable()
		for sub_data in data:
			address = chord_pb2.Address()
			address.id = sub_data[0]
			address.addr = sub_data[1]
			response.result.append(address)
		response.id = self_id
		return response

	def SaveData(self, request, context):
		print('ok')
		print(request.key)
		print(request.text)
		data = save(request.key, request.text)
		print(data)
		response = chord_pb2.ResponseAction()
		response.ok	= data[0]
		response.message = str(data[1])
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

	def Name(self, request, context):
		response = chord_pb2.Answer()
		response.name = "Connected to Node"
		return response


def Server():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
	chord_pb2_grpc.add_NodeServicer_to_server(ServiceHandler(), server)
	server.add_insecure_port(f'{ipaddr}:{port}')
	server.start()
	try:
		server.wait_for_termination()
	except KeyboardInterrupt:
		print("Shutting down")
		quit()

def main():
	global registry_ipaddr, registry_port, ipaddr, port
	registry_ipaddr, registry_port, ipaddr, port = getFromArgsNode(argv)

	try:
		channel = grpc.insecure_channel(f'{registry_ipaddr}:{registry_port}')
		msg = chord_pb2.RequestRegister(ipaddr=ipaddr, port=port)
		stub = chord_pb2_grpc.RegistryStub(channel)
		response = stub.Register(msg)
		if response.done != -1:
			global m, self_id
			self_id = response.done
			m = int(response.message)
			print(self_id, m)
		else:
			print(response.message)
			exit(1)

		thread = threading.Thread(target=Server, args=())
		thread.start()
		
		while True:
			try:
				time.sleep(1)
				channel = grpc.insecure_channel(f'{registry_ipaddr}:{registry_port}')
				msg = chord_pb2.RequestPopulateFingerTable(id=self_id)
				stub = chord_pb2_grpc.RegistryStub(channel)
				response = stub.PopulateFingerTable(msg)
				data = []
				for _address in response.result:
					data.append((_address.id, _address.addr))
				processUpdate(response.id)
				set_finger_table(data)
			except grpc.RpcError:
				print("You're not connected to regeistry")
				exit(1)
			except KeyboardInterrupt:
				print("Shutting down")
				quit()
	except grpc.RpcError:
		print("You're not connected to regeistry")
		exit(1)
	

if __name__ == '__main__':
	main()