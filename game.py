from tile import Tile
from options import Options
from counter import Counter

class Game():
    def __init__(self, opts):
        self.height = opts.opts["game"]["height"]
        self.width = opts.opts["game"]["width"]
        self.mines = opts.opts["game"]["mines"]
        self.board = [[Tile(x, y) for y in range(self.width)] for x in range(self.height)]
        
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
        temp = [(i, j) for j in range(self.width) for i in range(self.height) if i != x and j != y]
        temp.shuffle()
        for u, v in temp[:self.mines]:
            self.board[u][v].set_mine()

    def finish_check(self):
        for x in range(self.height):
            for y in range(self.width):
                if self.board[x][y].covered and not self.board[x][y].is_mine:
                    return False
        self.finish = True
        for x in range(self.height):
            for y in range(self.width):
                self.board[x][y].update_finish()
        return True

    def blast_check(self):
        for x in range(self.height):
            for y in range(self.width):
                if not self.board[x][y].covered and self.board[x][y].is_mine:
                    self.blast = True
        if self.blast:
            for x in range(self.height):
                for y in range(self.width):
                    self.board[x][y].update_blast()
        return self.blast

    def operate(func):
        def temp(self):
            if self.blast or self.finish:
                return
            func(self)
            if not self.finish_check() and not self.blast_check():
                for x in range(self.height):
                    for y in range(self.width):
                        self.board[x][y].update()            
        return temp
        
    @operate
    def left(self, x, y):
        if self.first:
            self.set_mine(x, y)
            self.first = False
        if self.opts["game_style"]["bfs"]:
            self.board[x][y].BFS_open()
        else:
            self.board[x][y].open()

    @operate
    def right(self, x, y):
        if not self.opts["game_style"]["nf"]:
            if self.opts["game_style"]["ez_flag"]:
                self.board[x][y].easy_flag()
            else:
                self.board[x][y].flag()

    @operate
    def double(self, x, y):
        if not self.opts["game_style"]["nf"]:
            if self.opts["game_style"]["bfs"]:
                self.board[x][y].BFS_double()
            else:
                self.board[x][y].double()

    @operate
    def left_hold(self, x, y):
        self.board[x][y].left_hold()

    @operate
    def double_hold(self, x, y):
        if not self.opts["game_style"]["nf"]:
            self.board[x][y].double_hold()

    def output(self):
        return [[self.board[x][y].status for y in range(self.width)] for x in range(self.height)]

    def __repr__(self):
        return '\n'.join(
            ''.join(
                str(self.board[x][y].status)
                for y in range(self.width)
            )
            for x in range(self.height)
        )

e = Game(Options())
print(e)