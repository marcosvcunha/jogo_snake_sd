import socket
import socket_communication as sc
import time
from datetime import datetime
import threading

HEADERSIZE = 10
SERVER_ADDR = '192.168.100.8' #socket.gethostname()
PORT = 1234


def start():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Iniciando conexão com o servidor...")
    s.connect((SERVER_ADDR, PORT))
    print('Esperando outros jogadores se conectarem...')
    start_msg = sc.rcv_msg(s)
    lastMsg = datetime.now().timestamp()
    print('Partida Iniciada')
    print(start_msg)
    game_over = False
    while(not game_over):
        msg = sc.rcv_msg(s)
        aux = datetime.now().timestamp()
        timePassed = aux - lastMsg
        lastMsg = aux
        print(f'Tempo decorrido: {timePassed}')
        if(msg == 'Partida Finalizada'):
            game_over = True
start()