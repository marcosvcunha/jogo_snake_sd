import socket
import math
import pickle
import time

HEADERSIZE = 2048

def send_msg(conn, msg):
    # msg_len = len(msg)
    # print(msg_len)
    # header = f'{msg_len:<{HEADERSIZE}}'
    # # print(HEADERSIZE)
    conn.send(msg)
    # conn.send(msg)

def rcv_msg(conn):
    try:
        msg_size = conn.recv(HEADERSIZE)##.decode('utf-8')
        # msg_size = int(msg_size)
        # print(pickle.loads(msg_size))
        return pickle.loads(msg_size)
    except:
        pass
        # print('Erro ao receber o Header')

    # try:
    #     msg = b''
    #     for _ in range(math.ceil(msg_size/HEADERSIZE)):
    #         msg += conn.recv(HEADERSIZE)
    #     return pickle.loads(msg)
    # except:
    #     pass
    #     # print('Erro ao receber o Body')