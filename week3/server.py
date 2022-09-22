import zmq
from sys import argv
import sys 


context = zmq.Context()
client_inputs = context.socket(zmq.REP)
client_outputs = context.socket(zmq.PUB)
worker_inputs = context.socket(zmq.PUB)
worker_outputs = context.socket(zmq.SUB)

C_INPUT_PORT, C_OUTPUT_PORT, W_INPUT_PORT, W_OUTPUT_PORT = argv[1:]   

C_INPUT_PORT = int(C_INPUT_PORT)
C_OUTPUT_PORT = int(C_OUTPUT_PORT)
W_INPUT_PORT = int(W_INPUT_PORT)
W_OUTPUT_PORT = int(W_OUTPUT_PORT)

client_inputs.bind(f"tcp://127.0.0.1:{C_INPUT_PORT}")
client_inputs.setsockopt(zmq.RCVTIMEO, 200)

client_outputs.bind(f"tcp://127.0.0.1:{C_OUTPUT_PORT}")

worker_inputs.bind(f"tcp://127.0.0.1:{W_INPUT_PORT}")

worker_outputs.bind(f"tcp://127.0.0.1:{W_OUTPUT_PORT}")
worker_outputs.setsockopt_string(zmq.SUBSCRIBE, '')
worker_outputs.setsockopt(zmq.RCVTIMEO, 200)


try:
    while True:
        try:
            msg = client_inputs.recv_string()
            try: 
                client_inputs.send_string(msg)
            except zmq.error.ZMQError:
                pass
            
            client_outputs.send_string(msg)
            worker_inputs.send_string(msg)
            while True:
                msg = worker_outputs.recv_string()
                client_outputs.send_string(msg)
        except zmq.Again:
            pass
                
except KeyboardInterrupt:
    client_inputs.close()
    client_outputs.close()
    worker_inputs.close()
    worker_outputs.close()
    sys.exit()







