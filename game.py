import pygame
import threading
import time
from button import Button

HEIGHT = 540
WIDTH = 840

class Game():
    def __init__(self):
        pygame.init()
        self.currentState = 'menu'
        self.win = pygame.display.set_mode((840, 540))
        self.doRun = True
        self.buttons = [
            Button(pygame, self.win, x=(WIDTH//2), y = (HEIGHT//2), height=60, width=150,
                 text='Iniciar Jogo', onPressed=self.doNothing, color=(0, 0, 0), textColor=(255, 255, 255))
        ]
    
    def doNothing(self):
        print('Clickou!!')

    def run(self):
        while(self.doRun):
            self.handle_events()
            self.draw_menu()

    def draw_menu(self):
        self.win.fill((255, 255, 255))
        for button in self.buttons:
            button.draw()
        
        pygame.display.update()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Encerrando o JOGO!!!')
                self.gameOver = True
                pygame.quit()
            elif(event.type == pygame.MOUSEBUTTONDOWN):
                for button in self.buttons:
                    button.click(event.dict['pos'][0], event.dict['pos'][1])


game = Game()
game.run()

print('Jogo Encerrado!')

