import grpc 
import chord_pb2
import chord_pb2_grpc


connected_to = "not connected"
def connect(str):
	_, addr = str.split(' ')
	global channel, stub, response, connected_to
	msg = chord_pb2.Empty()
	try:
		channel = grpc.insecure_channel(addr)
		stub = chord_pb2_grpc.RegistryStub(channel)
		try:
			response = stub.Name(msg)
		except grpc.RpcError:
			stub = chord_pb2_grpc.NodeStub(channel)
			try:
				response = stub.Name(msg)
			except grpc.RpcError:
				print("not connected to both register and node")
	except Exception as error:
		print(error)	

	identity = response.name
	if 'Node' not in identity and 'Registry' not in identity:
		raise Exception("not connected to both register and node")
	connected_to = identity
	print(identity)

def get_info():
	if 'Registry' in connected_to:
		msg = chord_pb2.Empty()
		response = stub.GetChordInfo(msg)
		for node in response.result:
			print(node.id, ":          " , node.addr)
	else:
		msg = chord_pb2.Empty()
		response = stub.GetFingerTable(msg)
		print("Node id: ", response.id)
		print("Finger table:")
		for node in response.result:
			print(node.id, ":          " , node.addr)

def save(str):
	_, key_ = str.split(' ', 1)
	key, text = key_[1:].split('" ', 1)
	if 'Registry' in connected_to:
		print("In registry can't do this command")
	else:
		msg = chord_pb2.RequestSave()
		msg.key=key
		msg.text=text
		response = stub.SaveData(msg)
		print(response.ok, ",", response.message)

def remove(key):
	_, key = key.split(' ', 1)
	if 'Registry' in connected_to:
		print("In registry can't do this command")
	else:
		msg = chord_pb2.RequestRemove(key=key)
		response = stub.Remove(msg)
		print(response.ok, ",", response.message)

def find(key):
	_, key = key.split(' ', 1)
	if 'Registry' in connected_to:
		print("In registry can't do this command")
	else:
		msg = chord_pb2.RequestFind(key=key)
		response = stub.Find(msg)
		print(response.ok, ",", response.message)

def quit():
	exit() 

def main():
	try:
		while True:
			str = input()
			if "connect" in str:
				connect(str) 
			elif connected_to == "not connected":
				print("You're not connected! please connect to Node or Registry")
			elif str == "get_info":
				get_info()
			elif "save" in str:
				save(str)
			elif "find" in str:
				find(str)
			elif "remove" in str:
				remove(str)
			else:
				print("wrong format of inputing")
	except KeyboardInterrupt:
		pass 

if __name__ == '__main__':
	main()