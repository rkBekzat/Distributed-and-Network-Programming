from concurrent import futures
import grpc
import raft_pb2, raft_pb2_grpc
import sys, os


self_id = -1
self_addr = ""
self_port = 0

all_nodes = {}

def getDataFromConfig(id):
    try:
        file = open("config.conf", 'r')
        _data = file.read().split('\n')
        for _line in _data:
            line = _line.split(" ")
            all_nodes[line[0]] = f"{line[1]}:{line[2]}"
        for _line in _data:
            line = _line.split(" ")
            if str(line[0]) == str(id):
                return line[1], line[2]
    except Exception:
        pass
    raise f"Id {id} did not found in config"

def getArgs():
    global self_id, self_addr, self_port
    self_id = str(sys.argv[1])
    self_addr, self_port = getDataFromConfig()


def _RequestVote(trem, candidateID):
    pass
def _AppendEntries(trem, candidateID):
    pass

def _GetLeader():
    pass
def _Suspend(time):
    pass

def funFollower():
    pass

def funCandidate():
    pass

def funLeader():
    pass


class serverServicer(raft_pb2_grpc.serverServicer):
    def RequestVote(self, request, context):
        pass
    def AppendEntries(self, request, context):
        pass

class clientServicer(raft_pb2_grpc.clientServicer):
    def GetLeader(self, request, context):
        pass
    def Suspend(self, request, context):
        pass
        


# server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
# Example_pb2_grpc.add_ExampleServicer_to_server(
#     ExampleServicer(),
#     server)
# server.add_insecure_port(SERVER_ADDRESS)

# server.start()
# server.wait_for_termination()