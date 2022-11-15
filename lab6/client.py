import grpc 
import raft_pb2
import raft_pb2_grpc


isConnected = "not connected"
def connect(str):
    _, addr, port = str.split(' ')
    global channel, stub, response, isConnected
    try:
        channel = grpc.insecure_channel(f"{addr}:{port}")
        stub = raft_pb2_grpc.serverStub(channel)
    except Exception as error:
        print(error)	
    isConnected='connected'


def getLeader():
    msg = raft_pb2.Empty()
    response = stub.GetLeader(msg)
    print(f"ID: {response.id}, Address: {response.address}")

def suspend(str):
    _, period = str.split(' ')
    msg = raft_pb2.RequestPeriod(period=period)
    response = stub.Suspend(msg)


def main():
    try:    
        while True:
            func = input()
            if "connect" in func:
                connect(func)
            elif isConnected == "not connected":
                print("Client not connected to server")
            elif "getleader" == func:
                getLeader()
            elif "suspend" in func:
                suspend(func)
            else:
                print("this function doesn't exist")
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    main()

