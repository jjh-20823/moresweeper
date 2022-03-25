from tile import Tile
# from options import Options
from counter import Counter

class Game():
    def __init__(self, opts):
        self.height = opts.height
        self.width = opts.width
        self.mines = opts.mines
        self.board = [[Tile(x, y) for y in range(opts.width)] for x in range(opts.height)]
        
        self.first = True
        self.finish = False
        self.blast = False

        self.opts = opts

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

    def check_game(self, func):
        if self.blast or self.finish:
            return
        func()
        



    def left(self, x, y):
        if self.blast or self.finish:
            return
        if self.first:
            self.set_mine(x, y)
        if self.opts["game_style"]["bfs"]:
            self.board[x][y].BFS_open()
        else:
            self.board[x][y].open()

    def right(self, x, y):
        if self.blast or self.finish:
            return
        if not self.opts["game_style"]["nf"]:
            if self.opts["game_style"]["ez_flag"]:
                self.board[x][y].easy_flag()
            else:
                self.board[x][y].flag()

    def double(self, x, y):
        if self.blast or self.finish:
            return
        if not self.opts["game_style"]["nf"]:
            if self.opts["game_style"]["bfs"]:
                self.board[x][y].BFS_double()
            else:
                self.board[x][y].double()

    # def left_hold(x, y):
