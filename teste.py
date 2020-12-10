from game_files.snake import Direction

segments = [[3, 0], [2, 0], [1, 0], [0, 0]]
direction = Direction.RIGHT

def move():
    lastPos = segments[0].copy()
    if(direction == Direction.UP):
        segments[0][1] -= 1
    elif(direction == Direction.RIGHT):
        segments[0][0] += 1
    elif(direction == Direction.DOWN):
        segments[0][1] += 1
    else:
        segments[0][0] -= 1
    for i in range(1, len(segments)):
        print(i)
        aux = segments[i].copy()
        segments[i] = lastPos
        lastPos = aux.copy()

move()