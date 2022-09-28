import grpc 
import time
import service_pb2
import service_pb2_grpc
from sys import argv
from asyncio import streams

def iterate(nums):
	for num in nums:
		yield service_pb2.isPrimeRequest(number=int(num))

def run():
	ADDRESS = argv[1:][0]
	with grpc.insecure_channel(f'{ADDRESS}') as channel:
		stub = service_pb2_grpc.calculateStub(channel)
		while True:
			request = input('> ')
			try:
				if request[:5] == "split":
					split_request = service_pb2.splitRequest(text=request[6:], delim=' ')
					split_reply = stub.split(split_request)
					print(split_reply)	

				elif request[:7] == "isprime":
					numbers = request[8:].split()
					isprime_reply = stub.isprime(iterate(numbers))
					for response in isprime_reply:
						print(response.message)

				elif request[:7] == "reverse":
					reverse_request = service_pb2.Message(message=request[8:])
					reverse_reply = stub.reverse(reverse_request)
					print(reverse_reply)
				elif request == "exit":
					print("Shutting down")
					break
			except ValueError:
				continue

if __name__ == '__main__':
	run()
