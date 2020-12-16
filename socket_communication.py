import socket
import math
import pickle
import time

HEADERSIZE = 512

def send_msg(conn, msg):
    msg_len = len(msg)
    header = f'{msg_len:<{HEADERSIZE}}'
    # print(HEADERSIZE)
    conn.send(header.encode('utf-8'))
    conn.send(msg)

def rcv_msg(conn):
    try:
        msg_size = conn.recv(HEADERSIZE).decode('utf-8')
        msg_size = int(msg_size)
    except:
        pass
        # print('Erro ao receber o Header')

    try:
        msg = b''
        for _ in range(math.ceil(msg_size/HEADERSIZE)):
            msg += conn.recv(HEADERSIZE)
        return pickle.loads(msg)
    except:
        pass
        # print('Erro ao receber o Body')