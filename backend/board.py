"""Board: A number of tiles."""

from .tile import Tile
from .stats import *
from random import shuffle
from copy import deepcopy
from time import perf_counter_ns as time


class Board(object):
    """Board: A number of tiles."""

    def __init__(self, settings: any):
        """Initialize a board."""
        self.opts: any = settings
        self.height: int = self.opts.height  # height
        self.width: int = self.opts.width  # width
        self.tile_count: int = self.height * self.width
        self.mines: int = self.opts.mines  # mines
        self.init_tiles()

    def xy_index(self, x, y):
        return x * self.width + y

    def in_board(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width

    def get_tile(self, x, y):
        return self.tiles[self.xy_index(x, y)] if self.in_board(x, y) else None

    def get_tiles(self, pairs):
        tiles = set(self.get_tile(*pair) for pair in pairs)
        tiles.discard(None)
        return tiles

    def set_neighbours(self):
        for tile in self.tiles:
            tile.neighbours = self.get_tiles(
                ((tile.x + i, tile.y + j) for i in (-1, 0, 1)
                for j in (-1, 0, 1)))
            tile.neighbours.remove(tile)

    def init(self):
        """Initialize the board."""
        self.finish: bool = False
        self.blast: bool = False
        self.stats = [0 for _ in range(stats_count)]
        self.marker = [
            [] for _ in range(self.height) for __ in range(self.width)
        ]
        self.op_counter = [0 for _ in range(self.tile_count)]
        self.is_counter = [0 for _ in range(self.tile_count)]

    def init_tiles(self):
        self.tiles: list[Tile] = [
            Tile(x, y) for x in range(self.height) for y in range(self.width)
        ]  # tiles
        self.set_neighbours()
        self.init()

    def set_mines(self, x, y):
        """Set mines for the board."""
        mine_field = [i for i in range(self.tile_count) if i != self.xy_index(x, y)]
        shuffle(mine_field)  # shuffle the field

        for i in mine_field[:self.mines]:
            self.tiles[i].set_mine()  # toggle mine value
        self.calc_basic_stats()

    def recover(self):
        for tile in self.tiles:
            tile.recover()
        self.init()

    def release(self):
        for tile in self.tiles:
            tile.unhold()

    def finish_check(self):
        for tile in self.tiles:
            if tile.covered and not tile.is_mine():
                return False
        self.finish = True
        return True

    def blast_check(self):
        for tile in self.tiles:
            if not tile.covered and tile.is_mine():
                self.blast = True
        return self.blast

    def end_check(self):
        return self.blast_check() or self.finish_check()

    def board_operate(func):

        def inner(self, x: int, y: int, *args):
            self.release()
            changed_tiles = set()
            if self.in_board(x, y):
                changed_tiles = func(self, self.xy_index(x, y), *args)
            changed_tiles |= self.get_tiles(
                ((x + i, y + j) for i in range(-2, 3)
                for j in range(-2, 3)))
            self.end_check()
            return changed_tiles

        return inner

    @board_operate
    def left(self, index, BFS):
        return self.tiles[index].open(BFS)

    @board_operate
    def right(self, index, easy_flag):
       return self.tiles[index].flag(easy_flag=True)

    @board_operate
    def double(self, index, BFS):
        return self.tiles[index].double(BFS)

    @board_operate
    def left_hold(self, index):
        self.tiles[index].left_hold()
        return set()

    @board_operate
    def double_hold(self, index):
        self.tiles[index].double_hold()
        return set()

    def output(self):
        return [(t.x, t.y, t.status) for t in self.tiles]

    # @staticmethod()
    # def has_op(tiles: set[Tile]):
    #     for t in tiles:
    #         if t.value == 0 and t.covered:
    #             return True
    #     return False

    # @staticmethod()
    # def has_bv(tiles: set[Tile]):
    #     for t in tiles:
    #         if t.value != -1 and t.covered:
    #             return True
    #     return False

    def calc_basic_stats(self):
        temp_tiles = self.tiles
        op_num, is_num = 1, -1
        for t in temp_tiles:
            if t.value == 0 and t.covered:
                op = t.open(BFS=False, test_op=True)
                for tt in op:
                    self.marker[self.xy_index(tt.x, tt.y)].append(op_num)
                    self.op_counter[op_num] += 1
                op_num += 1
        self.stats[STATS.OP] = op_num - 1
        self.stats[STATS.BBBV] = self.stats[STATS.OP]
        for t in temp_tiles:
            if t.value == -1:
                t.flag()
            elif t.value != -1 and t.covered:
                self.stats[STATS.BBBV] += 1
        for t in temp_tiles:
            if t.value != -1 and t.covered:
                is_ = t.open(BFS=True)
                for tt in is_:
                    self.marker[self.xy_index(tt.x, tt.y)].append(is_num)
                    self.is_counter[is_num] += 1
                is_num -= 1
        self.stats[STATS.IS] = -1 - is_num
        for tile in temp_tiles:
            tile.recover()

    def calc_in_game_stats(self):
        ...

    def calc_finish_stats(self):
        ...

    def __repr__(self):
        return '\n'.join(''.join(
            str(self.get_tile(x, y).status) for y in range(self.width))
                         for x in range(self.height)) + '\n'
