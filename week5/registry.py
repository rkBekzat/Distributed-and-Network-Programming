import grpc	
import chord_pb2
import chord_pb2_grpc
from concurrent import futures
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
	list_id = sorted(list(chord_info.keys()))
	for _id in list_id:
		if _id >= id % 2**m:
			return _id
	if len(list_id) > 0:
		return sorted(list_id)[0]
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
	for i in range(m):
		finger_ids[findNext((id + 2 ** i) % (2**m), id)] = i

	if id in finger_ids:
		del finger_ids[id]

	result_list = []
	for _id in finger_ids.keys():
		result_list.append((_id, f"{chord_info[_id][0]}:{chord_info[_id][1]}"))
	this_id_pos = -1
	list_id = sorted(list(chord_info.keys()))
	for _id in range(len(list_id)):
		if list_id[_id] == id:
			this_id_pos = _id
			break
	process_id = list_id[(this_id_pos - 1 + len(list_id)) % len(list_id)]
	return process_id, result_list


def get_chord_info():
	result = []
	for id in chord_info.keys():
		result.append((id, f"{chord_info[id][0]}:{chord_info[id][1]}"))
	return result

class ServiceHandler(chord_pb2_grpc.RegistryServicer):
	def Register(self, request, context):
		data = register(request.ipaddr, request.port)
		response = chord_pb2.ResponseRegister()
		response.done = data[0]
		response.message = str(data[1])
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

	def Name(self, request, context):
		response = chord_pb2.Answer()
		response.name = "Connected to Registry"
		return response

	
def main():
	global ipaddr, port, m
	ipaddr, port, m = getFromArgsRegistry(argv)
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
	chord_pb2_grpc.add_RegistryServicer_to_server(ServiceHandler(), server)
	server.add_insecure_port(f'{ipaddr}:{port}')
	server.start()
	try:
		server.wait_for_termination()
	except KeyboardInterrupt:
		print("Shutting down")

if __name__ == '__main__':
	random.seed(0)
	main()


	