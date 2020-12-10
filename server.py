import socket
import time
import math
import socket_communication as sc
import threading
import pickle
from game_files.snake import Snake

HEADERSIZE = 10
N_PLAYERS = 1 # número de jogadores por partida
SERVER_ADDR = '192.168.100.8' #socket.gethostname()
# print(SERVER_ADDR)


class GameConnection():
    ## Game Connection é a classe que gerencia um jogo.
    ## Espera que um número X de jogadores se conecte, então inicia a partida.
    def __init__(self):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.bind((SERVER_ADDR, 1234))
        self.my_socket.listen(5)

        self.client_sockets = []
        self.client_addresses = []
        self.snakes = []   

    def wait_connection(self):
        ## Função espera a conexão de um certo número de jogadores para fechar o jogo.
        ## Recebe o IP de cada jogador.
        ## Assim que tiver um número certo de jogadores avisa quem será o Host
        ## e passa o IP do host para os outros jogadores.
        print("Iniciando partida.")
        print(f"Esperando {N_PLAYERS} jogadores se conectarem...")
        for i in range(N_PLAYERS):
            conn, address = self.my_socket.accept()
            self.client_sockets.append(conn)
            self.client_addresses.append(address)
            print(f"O jogadore do IP {address} se juntou a partida!")
            print(f"Esperando {N_PLAYERS - i - 1} jogadores se conectarem...")

        # msg = sc.rcv_msg(self.my_socket)

        for i in range(len(self.client_sockets)):
            msg = {
                'status':'Iniciando Partida',
                'player_id': i,
            }
            self.snakes.append(Snake(i))
            sc.send_msg(self.client_sockets[i], pickle.dumps(msg))
        time.sleep(0.2)

    def start_game(self):
        ## Iniciando:
        self.doRun = True
        snakeArray = []
        for snake in self.snakes:
            snakeArray.append(snake.segments)
        
        for i in range(3):
            msg = {
                'msg_type': 'game_msg',
                'msg': 'start_count',
                'snakes': snakeArray,
                'count': 3 - i
            }
            self.send_msg_to_all(msg)
            time.sleep(1)
        
        for i in range(len(self.client_sockets)):
            t = threading.Thread(target=self.receive_actions, args=(self.client_sockets[i],))
            t.start()


        for i in range(500):
            
            self.send_updated_objects()
            self.move_snakes()
            time.sleep(0.1)

        self.doRun = False
        msg = {
                'msg_type': 'game_msg',
                'msg' : 'Game Over'
        }
        self.send_msg_to_all(msg)

    
    def send_updated_objects(self):
        snakeArray = []
        for snake in self.snakes:
            snakeArray.append(snake.segments)
        
        msg = {
                'msg_type': 'game_update',
                'snakes': snakeArray,
        }
        self.send_msg_to_all(msg)

    def send_msg_to_all(self, msg):
        for i in range(len(self.client_sockets)):
            try:
                sc.send_msg(self.client_sockets[i], pickle.dumps(msg))
            except:
                print('Erro ao enviar mensagem')

    def move_snakes(self):
        ## Deve conferir se as cobras morreram ou comeram alguma comida
        ## Se sobrar apenas uma cobra, deve encerrar o jogo
        for snake in self.snakes:
            snake.move()

    def receive_actions(self, client_socket):
        ## utilizar semaforos
        while(client_socket != None):
            try:
                msg = sc.rcv_msg(client_socket)
                if(msg['type'] == 'user_action'):
                    direction = msg['new_direction']
                    player_id = msg['player_id']
                    for snake in self.snakes:
                        if(snake.player_id == player_id):
                            ## Confere se a direção não é oposta a atual (não é permitido virar 180°)
                            if(abs(direction.value - snake.direction.value) != 2):
                                snake.direction = direction
            except:
                client_socket = None
                print('Erro em receive_actions')

game = GameConnection()
game.wait_connection()
game.start_game()
