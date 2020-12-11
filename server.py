import socket
import time
import math
import socket_communication as sc
import threading
import pickle
from game_files.snake import Snake
import copy
import random
from datetime import datetime


# HEADERSIZE = 10
N_PLAYERS = 2 # número de jogadores por partida
SERVER_ADDR = '192.168.100.8' #socket.gethostname()
FRAME_TIME = 0.1
# print(SERVER_ADDR)
class Client():
    def __init__(self, socket, addr, player_id):
        self.socket = socket
        self.addr = addr
        self.id = player_id
        self.isConnected = True
        self.errorCounter = 0

class GameConnection():
    ## Game Connection é a classe que gerencia um jogo.
    ## Espera que um número X de jogadores se conecte, então inicia a partida.
    def __init__(self):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.bind((SERVER_ADDR, 1234))
        self.my_socket.listen(5)

        # self.client_sockets = []
        # self.client_addresses = []
        self.clients = []
        self.snakes = []
        self.foods = [[14, 14]]

    def wait_connection(self):
        ## Função espera a conexão de um certo número de jogadores para fechar o jogo.
        ## Recebe o IP de cada jogador.
        ## Assim que tiver um número certo de jogadores avisa quem será o Host
        ## e passa o IP do host para os outros jogadores.
        print("Iniciando partida.")
        print(f"Esperando {N_PLAYERS} jogadores se conectarem...")
        for i in range(N_PLAYERS):
            conn, address = self.my_socket.accept()
            # self.client_sockets.append(conn)
            # self.client_addresses.append(address)
            self.clients.append(Client(conn, address, i))
            print(f"O jogadore do IP {address} se juntou a partida!")
            print(f"Esperando {N_PLAYERS - i - 1} jogadores se conectarem...")

        # msg = sc.rcv_msg(self.my_socket)

        for client in self.clients:
            msg = {
                'status':'Iniciando Partida',
                'player_id': client.id,
            }
            self.snakes.append(Snake(client.id))
            sc.send_msg(client.socket, pickle.dumps(msg))
        time.sleep(0.2)

    def start_game(self):
        ## Iniciando:
        self.doRun = True
        # snakeArray = []
        # for snake in self.snakes:
            # snakeArray.append(snake.segments)
        
        snakes = [s.toDict() for s in self.snakes]

        for i in range(3):
            msg = {
                'msg_type': 'game_msg',
                'msg': 'start_count',
                'snakes': snakes,
                'foods': self.foods,
                'count': 3 - i
            }
            self.send_msg_to_all(msg)
            time.sleep(1)
        
        for client in self.clients:
            t = threading.Thread(target=self.receive_actions, args=(client,))
            t.start()

        self.lastFoodTime = datetime.now().timestamp()
        while(self.doRun):
            self.add_food()
            self.send_updated_objects()
            self.move_snakes()
            time.sleep(FRAME_TIME)

        # self.doRun = False
        msg = {
                'msg_type': 'game_msg',
                'msg' : 'Game Over'
        }
        self.send_msg_to_all(msg)

    
    def send_updated_objects(self):
        # snakeArray = []
        # for snake in self.snakes:
        #     snakeArray.append(snake.segments)
        snakes = [s.toDict() for s in self.snakes]
        msg = {
                'msg_type': 'game_update',
                'snakes': snakes,
                'foods': self.foods
        }
        self.send_msg_to_all(msg)

    def send_msg_to_all(self, msg):
        for client in self.clients:
            try:
                if(client.isConnected):
                    sc.send_msg(client.socket, pickle.dumps(msg))
            except:
                if(client.errorCounter == 0):
                    client.isConnected == False
                    self.killSnake(client.id)
                    ## TODO: remover cobra do usuário que saiu
                else:
                    client.errorCounter += 1
                print('Erro ao enviar mensagem')

    def move_snakes(self):
        ## Deve conferir se as cobras morreram ou comeram alguma comida
        ## Se sobrar apenas uma cobra, deve encerrar o jogo
        for snake in self.snakes:
            doMove = snake.move(self.snakes, self.foods)
            if(not doMove):
                ## A cobra acertou uma das paredes
                print("Acertou a parede!")
                self.foods = self.foods + snake.segments
                self.killSnake(snake.player_id)

    def add_food(self):
        ## adiciona uma nova comida

        # Adiciona uma nova comida a cada 50 ticks em média (5 segundos)
        auxTime = datetime.now().timestamp()
        if(auxTime - self.lastFoodTime >= 5):

            foodAdded = True
            # Confere se a comida não se localiza dentro de uma cobra ou outra comida
            newFood = [random.randint(0, 29), random.randint(0, 29)]
            for snake in self.snakes:
                for segment in snake.segments:
                    if(newFood == segment):
                        foodAdded = False
            
            for food in self.foods:
                if(food == newFood):
                    foodAdded = False

            while(not foodAdded):
                foodAdded = True
                newFood = [random.randint(0, 29), random.randint(0, 29)]
                for snake in self.snakes:
                    for segment in snake.segments:
                        if(newFood == segment):
                            foodAdded = False
                
                for food in self.foods:
                    if(food == newFood):
                        foodAdded = False
            
            self.foods.append(newFood)
            self.lastFoodTime = auxTime



    def killSnake(self, player_id):
        self.snakes = [snake for snake in self.snakes if snake.player_id != player_id]
        if(len(self.snakes) == 0):
            self.doRun = False

    def receive_actions(self, client):
        ## utilizar semaforos
        while(client.isConnected):
            try:
                msg = sc.rcv_msg(client.socket)
                if(msg['type'] == 'user_action'):
                    direction = msg['new_direction']
                    player_id = msg['player_id']
                    for snake in self.snakes:
                        if(snake.player_id == player_id):
                            ## Confere se a direção não é oposta a atual (não é permitido virar 180°)
                            print(snake.lastDirection)
                            if(abs(direction.value - snake.lastDirection.value) != 2):
                                snake.direction = direction
                elif(msg['type'] == 'user_left'):
                    ## Remove a cobra do jogador que saiu
                    print("Jogador Saiu!!")
                    self.snakes = [snake for snake in self.snakes if snake.player_id != msg['player_id']]
                    client.isConnected = False
                    self.killSnake(client.id)
            except Exception as e:
                client.isConnected = False
                self.killSnake(client.id)
                print('Erro em receive_actions')
                print(str(e))
        print('Parando de receber Ações!')

game = GameConnection()
game.wait_connection()
game.start_game()
