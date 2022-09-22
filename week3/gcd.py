import zmq
from sys import argv
import sys

context = zmq.Context()
worker_outputs = context.socket(zmq.PUB)
worker_inputs = context.socket(zmq.SUB)

INPUT_PORT, OUTPUT_PORT = argv[1:]
INPUT_PORT = int(INPUT_PORT)
OUTPUT_PORT = int(OUTPUT_PORT)

worker_inputs.connect(f"tcp://127.0.0.1:{INPUT_PORT}")
worker_inputs.setsockopt_string(zmq.SUBSCRIBE, 'gcd')

worker_outputs.connect(f"tcp://127.0.0.1:{OUTPUT_PORT}")


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b) 

try:
    while True:
        try:
            msg = worker_inputs.recv_string()
            _, a, b = msg.split()
            print(f'Received message: {msg}')
            a = int(a)
            b = int(b)
            worker_outputs.send_string(f"gcd for {a} {b}  is {gcd(a, b)}")
        except ValueError:
            continue
             
except KeyboardInterrupt:
    worker_inputs.close()
    worker_outputs.close()
    sys.exit()
