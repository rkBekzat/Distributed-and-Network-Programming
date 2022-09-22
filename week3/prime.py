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
worker_inputs.setsockopt_string(zmq.SUBSCRIBE, 'isprime')
worker_outputs.connect(f"tcp://127.0.0.1:{OUTPUT_PORT}")


def is_prime(x):
    if x <= 1 or x % 2 == 0 and x != 2:
        return f'{x} is not prime'
    for i in range(3, x, 2):
        if x % i == 0:
            return f'{x} is not prime'
        if i * i >= x:               # when i reach sqrt of n  we can stop check cause doesn't exist divider  
            return f'{x} is prime'


try:
    while True:
        try:
            msg = worker_inputs.recv_string()
            print(f'Received message: {msg}')
            _, num = msg.split(' ', 1)
            num = int(num)
            worker_outputs.send_string(is_prime(num))
        except ValueError:
            continue
except KeyboardInterrupt:
    worker_inputs.close()
    worker_outputs.close()
    sys.exit()