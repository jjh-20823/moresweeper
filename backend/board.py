"""Board: A number of tiles."""

from .tile import Tile
from .counter import Counter
from random import shuffle


class Board(object):
    """Board: A number of tiles."""

    def __init__(self, options: dict):
        """Initialize a board."""
        self.opts: dict = options  # load options
        self.height: int = self.opts["height"]  # height
        self.width: int = self.opts["width"]  # width
        self.tile_count: int = self.height * self.width
        self.mines: int = self.opts["mines"]  # mines
        self.init()

    def xy_index(self, x, y):
        return x * self.width + y

    def in_board(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width
    
    def get_tile(self, x, y):
        return self.tiles[self.xy_index(x, y)] if self.in_board(x, y) else None

    def set_neighbours(self):
        for tile in self.tiles:
            tile.neighbours = set(
                self.get_tile(tile.x + i, tile.y + j) for i in (-1, 0, 1)
                for j in (-1, 0, 1))
            tile.neighbours.remove(tile)
            tile.neighbours.discard(None)

    def init(self):
        """Initialize the board."""
        self.tiles: list[Tile] = [
            Tile(x, y) for x in range(self.height) for y in range(self.width)
        ]  # tiles
        self.first: bool = True
        self.finish: bool = False
        self.blast: bool = False
        self.upk: bool = False

        self.set_neighbours()

    def set_mines(self, index):
        """Set mines for the board."""
        if self.upk:
            return
        mine_field = [i for i in range(self.tile_count) if i != index]
        shuffle(mine_field)  # shuffle the field

        for i in mine_field[:self.mines]:
            self.tiles[i].set_mine()  # toggle mine value

        self.tiles[index].set_value()
        for i in mine_field[self.mines:]:
            self.tiles[i].set_value()  # calculate normal value

    def init_upk(self):
        """Toggle UPK mode."""
        self.upk = True
        for tile in self.tiles:
            tile.recover()
        self.first = True
        self.finish = False
        self.blast = False

    def finish_check(self):
        for tile in self.tiles:
            if tile.covered and not tile.is_mine():
                return False
        self.finish = True
        for tile in self.tiles:
            tile.update_finish()
        return True

    def blast_check(self):
        for tile in self.tiles:
            if not tile.covered and tile.is_mine():
                self.blast = True
        if self.blast:
            for tile in self.tiles:
                tile.update_blast()
        return self.blast

    def operate(func):
        def inner(self, x, y):
            if self.blast or self.finish:
                return
            for tile in self.tiles:
                tile.unhold()
            if self.in_board(x, y):
                func(self, self.xy_index(x, y))
            if not self.blast_check() and not self.finish_check():
                for tile in self.tiles:
                    tile.update()
        return inner

    @operate
    def left(self, index):
        if self.first:
            self.set_mines(index)
            self.first = False
        if self.opts["bfs"]:
            self.tiles[index].BFS_open()
        else:
            self.tiles[index].open()

    @operate
    def right(self, index):
        if not self.opts["nf"]:
            if self.opts["ez_flag"]:
                self.tiles[index].flag(easy_flag=True)
            else:
                self.tiles[index].flag()

    @operate
    def double(self, index):
        if not self.opts["nf"]:
            if self.opts["bfs"]:
                self.tiles[index].BFS_double()
            else:
                self.tiles[index].double()

    @operate
    def left_hold(self, index):
        self.tiles[index].left_hold()

    @operate
    def double_hold(self, index):
        if not self.opts["nf"]:
            self.tiles[index].double_hold()

    def output(self):
        return [[self.get_tile(x, y).status for y in range(self.width)]
                for x in range(self.height)]

    def __repr__(self):
        return '\n'.join(''.join(
            str(self.get_tile(x, y).status) for y in range(self.width))
                         for x in range(self.height)) + '\n'
