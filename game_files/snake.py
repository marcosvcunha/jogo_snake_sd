from enum import Enum

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
    
    def move(self):


        lastPos = self.segments[0].copy()

        if(self.direction == Direction.UP):
            self.segments[0][1] -= 1
        elif(self.direction == Direction.RIGHT):
            self.segments[0][0] += 1
        elif(self.direction == Direction.DOWN):
            self.segments[0][1] += 1
        else:
            self.segments[0][0] -= 1

        for i in range(1, len(self.segments)):
            print(i)
            aux = self.segments[i].copy()
            self.segments[i] = lastPos
            lastPos = aux.copy()

