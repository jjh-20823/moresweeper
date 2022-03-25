from tile import Tile

class Game():
    def __init__(self, height, width, mines):
        self.height = height
        self.width = width
        self.mines = mines
        self.board = [[Tile(x, y) for y in range(width)] for x in range(height)]
        self.first = False
        self.finish = False
        self.blast = False

    def set_neighbours(self):
        for x in range(self.height):
            for y in range(self.width):
                up = 0 if x == 0 else -1
                down = 0 if x == self.height - 1 else 1
                left = 0 if y == 0 else -1
                right = 0 if y == self.width - 1 else 1
                self.board[x][y].neighbours = set(
                    self.board[x + i][y + j]
                    for i in range(up, down + 1)
                    for j in range(left, right + 1)
                )
                self.board[x][y].neighbours.remove(self.board[x][y])
    
    def set_mine(self, x, y):
        ...

    # def left