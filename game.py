import pygame
import threading
import time
from button import Button
import pickle
import socket
import socket_communication as sc
import time
from datetime import datetime
import threading

from game_files.snake import Direction, Snake

HEADERSIZE = 10
SERVER_ADDR = '192.168.100.8' #socket.gethostname()
PORT = 1234


## Função do lado do cliente que mostra a tela do jogo e captura os eventos

HEIGHT = 600
WIDTH = 600
SQUARE_SIZE = 20

class Game():
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.doRun = True
        self.currentState = 'menu'
        self.buttons = [
            Button(pygame, self.win, x=(WIDTH//2), y = (HEIGHT//2), height=60, width=150,
                 text='Iniciar Jogo', onPressed=self.start_request, color=(0, 0, 0), textColor=(255, 255, 255))
        ]
        self.draw_menu()
        # self.stateLock = threading.Lock() # Lock para leitura do estado

    def start_request(self):
        ## Função chamada quando o usuário clica em "Iniciar jogo" no menu
        ## TODO: Implementar função para iniciar o jogo.
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Iniciando conexão com o servidor...")
        self.s.connect((SERVER_ADDR, PORT))
        print('Esperando outros jogadores se conectarem...')
        
        self.currentState = 'waiting'
        self.buttons = [
            Button(pygame, self.win, x=(WIDTH//2), y = (HEIGHT//2), height=60, width=150,
                 text='Esperando o jogo iniciar...', onPressed=self.doNothing, color=(255, 255, 255), textColor=(0, 0, 0))
        ]
        self.draw_menu()

        start_msg = sc.rcv_msg(self.s)
        self.player_id = start_msg['player_id']

        self.currentState = 'playing'
        self.buttons = [
            Button(pygame, self.win, x=(WIDTH//2), y = (HEIGHT//2), height=60, width=150,
                 text='Jogo Iniciado', onPressed=self.doNothing, color=(255, 255, 255), textColor=(0, 0, 0))
        ]

        self.draw_menu()

        t = threading.Thread(target=self.receive_update)
        t.start()
        
    
    def receive_update(self):
        starting_msg = Button(pygame, self.win, x=(WIDTH//2), y = (HEIGHT//2), height=60, width=150,
                 text='O jogo vai iniciar em: ', onPressed=self.doNothing, color=(255, 255, 255), textColor=(0, 0, 0))
        while(self.doRun):
            try:
                game_update = sc.rcv_msg(self.s)
                if(game_update['msg_type'] == 'game_update'):
                    snakes = game_update['snakes']
                    foods = game_update['foods']
                    self.draw_board(snakes, foods)
                else:
                    if(game_update['msg'] == 'Game Over'):
                        self.doRun = False
                        pygame.quit()
                    elif(game_update['msg'] == 'start_count'):
                        snakes = game_update['snakes']
                        foods = game_update['foods']
                        self.draw_board(snakes, foods)
                        count = game_update['count']
                        starting_msg.setText('O jogo vai iniciar em: ' + str(count))
                        starting_msg.draw()
                        pygame.display.update()
            except Exception as e:
                print('Exceção em receive_update')
                print(str(e))

    def doNothing(self):
        pass

    def run(self):
        while(self.doRun):
            self.handle_events()



    def draw_menu(self):
        self.win.fill((255, 255, 255))
        for button in self.buttons:
            button.draw()
        
        pygame.display.update()
    
    def draw_board(self, snakes, foods):
        self.win.fill((255, 255, 255))
        for snake in snakes:
            if(snake['player_id'] == self.player_id):
                color = (35, 41, 158)
            else:
                color = (0, 0, 0)
            for square in snake['segments']:
                pygame.draw.rect(self.win, color, (square[0]*SQUARE_SIZE, square[1]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            for food in foods:
                pygame.draw.rect(self.win, (252, 186, 3), (food[0]*SQUARE_SIZE + 2, food[1]*SQUARE_SIZE + 2, SQUARE_SIZE - 4, SQUARE_SIZE - 4))
        pygame.display.update()
        


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Encerrando o JOGO!!!')
                self.send_exit_warning()
                self.doRun = False
                pygame.quit()
            elif(event.type == pygame.MOUSEBUTTONDOWN):
                for button in self.buttons:
                    button.click(event.dict['pos'][0], event.dict['pos'][1])
            elif(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_UP):
                    self.send_action(Direction.UP)
                elif(event.key == pygame.K_RIGHT):
                    self.send_action(Direction.RIGHT)
                elif(event.key == pygame.K_DOWN):
                    self.send_action(Direction.DOWN)
                elif(event.key == pygame.K_LEFT):
                    self.send_action(Direction.LEFT)
    
    def send_exit_warning(self):
        msg = {
            'type': 'user_left',
            'player_id': self.player_id,
        }

        sc.send_msg(self.s, pickle.dumps(msg))


    def send_action(self, direction):
        print('Enviando Ação!!')
        msg = {
            'type': 'user_action',
            'new_direction': direction,
            'player_id':self.player_id,
        }

        sc.send_msg(self.s, pickle.dumps(msg))
    


game = Game()
game.run()

print('Jogo Encerrado!')

