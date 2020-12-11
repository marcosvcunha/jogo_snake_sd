from enum import Enum
import copy
INITIAL_SIZE = 4

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Snake():
    def __init__(self, player_id):
        self.player_id = player_id

        if(player_id == 0):
            self.segments = [[3, 2], [2, 2], [1, 2], [0, 2]]
            self.direction = Direction.RIGHT
        elif(player_id == 1):
            self.segments = [[26, 4], [27, 4], [28, 4], [29, 4]]
            self.direction = Direction.LEFT
        elif(player_id == 2):
            self.segments = [[26, 25], [27, 25], [28, 25], [29, 25]]
            self.direction = Direction.LEFT
        else:
            self.segments = [[3, 27], [2, 27], [1, 27], [0, 27]]
            self.direction = Direction.RIGHT
        
        self.lastDirection = copy.copy(self.direction)

    def move(self, allSnakes, foods):

        self.lastDirection = copy.copy(self.direction)
        
        lastPos = self.segments[0].copy()
        head = self.segments[0].copy()

        if(self.direction == Direction.UP):
            head[1] -= 1
        elif(self.direction == Direction.RIGHT):
            head[0] += 1
        elif(self.direction == Direction.DOWN):
            head[1] += 1
        else:
            head[0] -= 1

        if(head[0] < 0 or head[0] >= 30 or head[1] < 0 or head[1] >= 30):
            ## Bateu numa parede
            return False
        else:
            didHit = False
            for snake in allSnakes:
                for segment in snake.segments:
                    if(segment == head):
                        didHit = True
            
            if(not didHit):
                # Confere se come alguma comida
                for food in foods:
                    if(head == food):
                        foods.remove(head)
                        self.segments.insert(0, head)
                        return True
                        
                self.segments[0] = head.copy()
                for i in range(1, len(self.segments)):
                    aux = self.segments[i].copy()
                    self.segments[i] = lastPos
                    lastPos = aux.copy()
                
                return True
            else:
                return False

            
    
    # def hit()        


    def toDict(self):
        return {
            'player_id': self.player_id,
            'segments': self.segments
        }
