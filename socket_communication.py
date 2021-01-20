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
    conn.send(pickle.dumps(msg))
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

def rcv_udp_msg(sock):
    try:
        msg, addr = sock.recvfrom(HEADERSIZE)
        # print(pickle.dumps(msg))
        # print(msg)
        return pickle.loads(msg)
    except Exception as e:
        print('Erro Ao Receber Mensagem!!!')
        print(e)

def send_udp_msg(sock, client, msg):
    try:
        # print(msg)
        sock.sendto(pickle.dumps(msg), client)
    except:
        pass