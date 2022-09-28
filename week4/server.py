import grpc  
import service_pb2
import service_pb2_grpc
from concurrent import futures
import time 
from sys import argv

def prime(x):
	x = int(x)
	if x == 1: return False
	if x == 2 or x == 3: return True
	for i in range(3, x):
		if x % i == 0:
			return False
		if i * i >= x:
			return True 

class ServiceHandler(service_pb2_grpc.calculateServicer):
	def isprime(self, request_iterator, context):
		for request in request_iterator:
			num = request.number 
			response = service_pb2.Message()
			if prime(num) == True:
				response.message = f'{num} is prime'
			else:
				response.message = f'{num} is not prime'
			yield response 

	def split(self, request, context):
		msg = request.text 
		splitter = request.delim
		splitted = msg.split(splitter)
		response = service_pb2.splitResponse()

		response.number = len(splitted)
		for part in splitted:
			response.parts.append(part)
		return response

	def reverse(self, request, context):
		msg = request.message
		response = service_pb2.Message()
		response.message = msg[::-1]
		return response


def serve():
	PORT = argv[1:][0]
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
	service_pb2_grpc.add_calculateServicer_to_server(ServiceHandler(), server)
	server.add_insecure_port(f'localhost:{PORT}')
	server.start()
	try:
		server.wait_for_termination()
	except KeyboardInterrupt:
		print('Shutting down')

if __name__ == '__main__':
	serve()

