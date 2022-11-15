import os
import random
import sys
import time
from concurrent import futures
from threading import Thread

import grpc

import raft_pb2
import raft_pb2_grpc

self_id = -1
self_addr = ""
self_port = 0

self_term_no = 0
self_voted = False
self_voted_me = 0
self_leader = False

leader = -1
wait_time = random.randint(150, 300)
restart = False 
all_nodes = {}

def getDataFromConfig(id):
    try:
        file = open("config.conf", 'r')
        _data = file.read().split('\n')
        for _line in _data:
            line = _line.split(" ")
            all_nodes[int(line[0])] = f"{line[1]}:{line[2]}"
        for _line in _data:
            line = _line.split(" ")
            if int(line[0]) == id:
                return line[1], line[2]
    except Exception:
        pass
    raise f"Id {id} did not found in config"

def getArgs():
    global self_id, self_addr, self_port
    self_id = int(sys.argv[1])
    self_addr, self_port = getDataFromConfig()


def _RequestVote(trem, candidateID):
    global self_term_no, self_voted, self_leader
    self_leader = False
    if self_term_no == trem:
        if self_voted:
            return False
        self_voted = True
        return True
    elif self_term_no < trem:
        self_voted = False
        self_term_no = trem
        return _RequestVote(trem, candidateID)
    return False
def _AppendEntries(trem, candidateID):
    global self_term_no, self_voted, leader, self_leader, restart
    self_leader = False
    if self_term_no <= trem:
        self_term_no = trem
        self_voted = False
        leader = candidateID
        restart = True
        return True
    return False
    

def _Suspend(time):
    pass

def funThrAppendForMe():
    global self_id, self_term_no
    for key in all_nodes.keys():
        if key != self_id:
            channel = grpc.insecure_channel(all_nodes[key])
            stub = raft_pb2_grpc.serverStub(channel)
            request = raft_pb2.Request(term = self_term_no, candidateID = self_id)
            stub.AppendEntries(request)

def funThrVoteForMe():
    global self_id, self_term_no, self_voted_me
    self_voted_me = 1
    for key in all_nodes.keys():
        if key != self_id:
            channel = grpc.insecure_channel(all_nodes[key])
            stub = raft_pb2_grpc.serverStub(channel)
            request = raft_pb2.Request(term = self_term_no, candidateID = self_id)
            responce = stub.RequestVote(request)
            if responce.vote:
                self_voted_me += 1

def waiting():
    global restart
    for i in range(wait_time):
            time.sleep(0.001)
            if restart == True:
                break
    return restart

def funFollower():
    global self_term_no, self_voted_me, self_leader, self_voted, restart
    is_Candidate = False
    is_Candidate_term = 0
    while True: 
        # TODO wait function
        if waiting():
            restart = False
            continue

        if is_Candidate and (is_Candidate_term != self_term_no or self_voted_me < len(all_nodes.keys())/2):
            is_Candidate = False
        if is_Candidate:
            self_leader = True
            is_Candidate = False
            funLeader()
        is_Candidate = True
        self_term_no += 1
        self_voted = True

        Thread(target=funThrVoteForMe).start()


def funLeader():
    global self_leader, leader, self_id, restart
    leader = self_id
    while self_leader:
        # TODO wait heart beat rate 
        if waiting():
            restart = False 
            continue

        Thread(target=funThrAppendForMe).start()
        pass
    self_leader = False


class serverServicer(raft_pb2_grpc.serverServicer):
    def RequestVote(self, request, context):
        global self_term_no
        responce = raft_pb2.Response()
        responce.term = self_term_no
        responce.vote = _RequestVote(int(request.term), int(request.candidateID))
        return responce

    def AppendEntries(self, request, context):
        global self_term_no
        responce = raft_pb2.Response()
        responce.term = self_term_no
        responce.vote = _AppendEntries(int(request.term), int(request.candidateID))
        return responce

    def GetLeader(self, request, context):
        global leader
        responce = raft_pb2.ResponseLeader()
        responce.id = leader
        responce.address = all_nodes[leader]
        return responce

    def Suspend(self, request, context):
        pass

        
def Server():
    getArgs()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    raft_pb2_grpc.add_serverServicer_to_server(serverServicer(), server)
    server.add_insecure_port(f"{self_addr}:{self_port}")
    server.start()
    server.wait_for_termination()

def ownFunc():
    while True:
        if self_leader:
            funLeader()
        else:
            funFollower()

def main():
    thread1 = Thread(target=Server, args=())
    thread2 = Thread(target=ownFunc, args=())
    thread1.start()
    thread2.start()


if __name__ == "__main__":
    main()
# server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
# Example_pb2_grpc.add_ExampleServicer_to_server(
#     ExampleServicer(),
#     server)
# server.add_insecure_port(SERVER_ADDRESS)

# server.start()
# server.wait_for_termination()