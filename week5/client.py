import grpc 
import chord_pb2
import chord_pb2_grpc


connected_to = "not connected"
def connect(str):
	_, addr = str.split(' ')
	global channel, stub
	msg = chord_pb2.Empty()
	response
	try:
		channel = grpc.insecure_channel(addr)
		stub = chord_pb2_grpc.RegisterStub(channel)
		try:
			response = stub.Name(msg)
		except grpc.RpcError:
			stub = chord_pb2_grpc.NodeStub(channel)
			try:
				response = stub.Name(msg)
			except grpc.RpcError:
				raise Exception("not connected to both register and node")
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
		# print(response)
	else:
		msg = chord_pb2.Empty()
		response = stub.GetFingerTable(msg)
		# print(response)

def save(str):
	key = ''
	pos = 1
	while str[pos] != str[0]:
		key += str[pos]
		pos += 1
	pos += 2

	text = str[pos:]
	if 'Registry' in connected_to:
		print("In registry can't do this command")
	else:
		msg = chord_pb2.RequestSave(key=key, text=text)
		response = stub.SaveData(msg)
		# print(response)

def remove(key):
	if 'Registry' in connected_to:
		print("In registry can't do this command")
	else:
		msg = chord_pb2.RequestRemove(key=key)
		response = stub.Remove(msg)
		# print(response)

def find(key):
	
	if 'Registry' in connected_to:
		print("In registry can't do this command")
	else:
		msg = chord_pb2.RequestFind(key=key)
		response = stub.Find(msg)
		# print(response)

def quit():
	pass 

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
				save(str[5:])
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