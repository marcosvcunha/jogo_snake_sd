import socket
import math
import pickle

HEADERSIZE = 10

def send_msg(conn, msg):
    msg_len = len(msg)
    header = f'{msg_len:<{HEADERSIZE}}'
    print(header)
    conn.send(header.encode('utf-8'))
    conn.send(msg)

def rcv_msg(conn):
    msg_size = conn.recv(HEADERSIZE).decode('utf-8')
    msg_size = int(msg_size)
    msg = b''
    for _ in range(math.ceil(msg_size/HEADERSIZE)):
        msg += conn.recv(HEADERSIZE)
    return pickle.loads(msg)