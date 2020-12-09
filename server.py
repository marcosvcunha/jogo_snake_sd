import socket
import time
import math
import socket_communication as sc
import threading
import pickle

HEADERSIZE = 10
N_PLAYERS = 3 # número de jogadores por partida
SERVER_ADDR = '192.168.100.8' #socket.gethostname()
# print(SERVER_ADDR)


class GameConnection():
    ## Game Connection é a classe que gerencia um jogo.
    ## Espera que um número X de jogadores se conecte, então inicia a partida.
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((SERVER_ADDR, 1234))
        self.s.listen(5)

        self.client_sockets = []
        self.client_addresses = []        

    def wait_connection(self):
        ## Função espera a conexão de um certo número de jogadores para fechar o jogo.
        ## Recebe o IP de cada jogador.
        ## Assim que tiver um número certo de jogadores avisa quem será o Host
        ## e passa o IP do host para os outros jogadores.
        print("Iniciando partida.")
        print(f"Esperando {N_PLAYERS} jogadores se conectarem...")
        for i in range(N_PLAYERS):
            conn, address = self.s.accept()
            self.client_sockets.append(conn)
            self.client_addresses.append(address)
            print(f"O jogadore do IP {address} se juntou a partida!")
            print(f"Esperando {N_PLAYERS - i - 1} jogadores se conectarem...")

        for sock in self.client_sockets:
            sc.send_msg(sock, pickle.dumps('Iniciando Partida'))
        
        for _ in range(5):
            for sock in self.client_sockets:
                sc.send_msg(sock, pickle.dumps('Wait'))

        for sock in self.client_sockets:
            sc.send_msg(sock, pickle.dumps('Partida Finalizada'))
            sock.close()            

game = GameConnection()
game.wait_connection()
