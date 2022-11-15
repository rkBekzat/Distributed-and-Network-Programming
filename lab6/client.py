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
    print(f"{response.id} {response.address}")

def suspend(str):
    _, period = str.split(' ')
    msg = raft_pb2.RequestPeriod(period=int(period))
    stub.Suspend(msg)


def main():
    try:    
        print("The client starts")
        while True:
            func = input()
            if "connect" in func:
                connect(func)
            elif isConnected == "not connected":
                print("Client not connected to server")
            elif "getLeader" == func:
                getLeader()
            elif "suspand" in func:
                suspend(func)
            elif "quit" == func:
                raise KeyboardInterrupt
            else:
                print("this function doesn't exist")
    except KeyboardInterrupt:
        print("The client ends")

if __name__ == '__main__':
    main()

