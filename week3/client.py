import zmq
from sys import argv
import sys 


context = zmq.Context()
client_inputs = context.socket(zmq.REQ)
client_outputs = context.socket(zmq.SUB)

INPUT_PORT, OUTPUT_PORT = argv[1:]
INPUT_PORT = int(INPUT_PORT)
OUTPUT_PORT = int(OUTPUT_PORT)

client_inputs.connect(f"tcp://127.0.0.1:{INPUT_PORT}")
client_inputs.setsockopt(zmq.RCVTIMEO, 300) 

client_outputs.connect(f"tcp://127.0.0.1:{OUTPUT_PORT}")
client_outputs.setsockopt_string(zmq.SUBSCRIBE, '')
client_outputs.setsockopt(zmq.RCVTIMEO, 300)


def send(message):
    global client_inputs
    try:
        client_inputs.send_string(message)
        try:
            client_inputs.recv_string()
            return "[Successfully sended]"
        except zmq.Again:
            pass
    except zmq.error.ZMQError:
        pass
        
    return "[Failed on sending]"
        
try:
    while True:
        line = input('> ')
        if len(line) != 0:
            print(send(line))
        try:
            while True:
                message = client_outputs.recv_string()
                print(f'Recieved message: {message}')
        except zmq.Again:
            pass
except KeyboardInterrupt:
    client_inputs.close()
    client_outputs.close()
    sys.exit()