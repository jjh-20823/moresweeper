from tile import Tile
from options import load_options
from counter import Counter
from random import shuffle

class Board():
    def __init__(self):
        self.opts = load_options("game_style")

        self.height, self.width = self.opts["height"], self.opts["width"]
        self.mines = self.opts["mines"]
        self.tiles = [[Tile(x, y) for y in range(self.width)] for x in range(self.height)]
        
        self.first = True
        self.finish = False
        self.blast = False

        self.set_neighbours()

    def set_neighbours(self):
        for x in range(self.height):
            for y in range(self.width):
                up = 0 if x == 0 else -1
                down = 0 if x == self.height - 1 else 1
                left = 0 if y == 0 else -1
                right = 0 if y == self.width - 1 else 1
                self.tiles[x][y].neighbours = set(
                    self.tiles[x + i][y + j]
                    for i in range(up, down + 1)
                    for j in range(left, right + 1)
                )
                self.tiles[x][y].neighbours.remove(self.tiles[x][y])
    
    def init(self, x, y):
        temp = [(i, j) for j in range(self.width) for i in range(self.height) if i != x and j != y]
        shuffle(temp)
        for u, v in temp[:self.mines]:
            self.tiles[u][v].set_mine()
        for x in range(self.height):
            for y in range(self.width):
                self.tiles[x][y].set_num()
                

    def finish_check(self):
        for x in range(self.height):
            for y in range(self.width):
                if self.tiles[x][y].covered and not self.tiles[x][y].is_mine:
                    return False
        self.finish = True
        for x in range(self.height):
            for y in range(self.width):
                self.tiles[x][y].update_finish()
        return True

    def blast_check(self):
        for x in range(self.height):
            for y in range(self.width):
                if not self.tiles[x][y].covered and self.tiles[x][y].is_mine:
                    self.blast = True
        if self.blast:
            for x in range(self.height):
                for y in range(self.width):
                    self.tiles[x][y].update_blast()
        return self.blast

    def operate(func):
        def temp(self, x, y):
            if self.blast or self.finish:
                return
            func(self, x, y)
            if not self.finish_check() and not self.blast_check():
                for x in range(self.height):
                    for y in range(self.width):
                        # self.tiles[x][y].unhold()
                        self.tiles[x][y].update()            
        return temp
        
    @operate
    def left(self, x, y):
        # self.tiles[x][y].left_unhold()
        if self.first:
            self.init(x, y)
            self.first = False
        if self.opts["bfs"]:
            self.tiles[x][y].BFS_open()
        else:
            self.tiles[x][y].open()

    @operate
    def right(self, x, y):
        if not self.opts["nf"]:
            if self.opts["ez_flag"]:
                self.tiles[x][y].easy_flag()
            else:
                self.tiles[x][y].flag()

    @operate
    def double(self, x, y):
        # self.tiles[x][y].double_unhold()
        if not self.opts["nf"]:
            if self.opts["bfs"]:
                self.tiles[x][y].BFS_double()
            else:
                self.tiles[x][y].double()

    @operate
    def left_hold(self, x, y):
        for i in range(self.height):
            for j in range(self.width):
                self.tiles[i][j].unhold()
        self.tiles[x][y].left_hold()

    # @operate
    # def left_unhold(self, x, y):
    #     self.tiles[x][y].left_unhold()

    @operate
    def double_hold(self, x, y):
        if not self.opts["nf"]:
            for i in range(self.height):
                for j in range(self.width):
                    self.tiles[i][j].unhold()
            self.tiles[x][y].double_hold()
    
    # @operate
    # def double_unhold(self, x, y):
    #     self.tiles[x][y].double_unhold()

    def output(self):
        return [[self.tiles[x][y].status for y in range(self.width)] for x in range(self.height)]

    def __repr__(self):
        return '\n'.join(
            ''.join(
                str(self.tiles[x][y].status)
                for y in range(self.width)
            )
            for x in range(self.height)
        ) + '\n'
# e = Board()
# print(e)
# e.left(0, 0)
# print('\n')
# print(e)