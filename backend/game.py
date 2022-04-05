"""Board: A number of tiles."""

from .tile import Tile
from .counter import Counter
from .board import Board
from random import shuffle


class Game(object):
    """Board: A number of tiles."""

    def __init__(self, settings: any):
        """Initialize a board."""
        self.opts: any = settings
        
        self.init()

    def init(self):
        """Initialize the board."""
        self.board = Board(self.opts)
        self.first: bool = True
        self.upk: bool = False
        self.stable: bool = False
        self.recently_updated: list[Tile] = self.board.tiles.copy()
        # self.holding: set(Tile) = set()
        # self.counter: Counter = Counter()

    def set_mines(self, index):
        """Set mines for the board."""
        if not self.upk:
            self.board.set_mines(index)  # don't need to update the mine field when it is UPK mode
        
    def init_upk(self):
        """Toggle UPK mode."""
        self.upk = True
        self.board.recover()
        self.stable = False
        self.recently_updated = self.board.tiles.copy()
        self.first = True

    def first_click(self, index):
        self.set_mines(index)
        # self.counter.start_timer()
        self.first = False

    def end(self):
        self.stable = False
        if self.board.blast:
            for tile in self.board.tiles:
                tile.update_blast()
        else:
            for tile in self.board.tiles:
                tile.update_finish()

    def operate(func):

        def inner(self, x, y):
            if self.board.blast or self.board.finish:
                return
            self.board.release()
            changed_tiles = set()
            if self.board.in_board(x, y):
                changed_tiles, button = func(self, self.board.xy_index(int(x), int(y)))
                # self.counter.update_ce_cl(changed_tiles, button)
            changed_tiles |= self.board.get_tiles(
                ((x + i, y + j) for i in range(-2, 3)
                for j in range(-2, 3)))
            if not self.board.end_check():
                self.stable = True
                for tile in changed_tiles:
                    tile.update()
                self.recently_updated = changed_tiles
            else:
                self.end()

        return inner

    @operate
    def left(self, index):
        if self.first:
            self.first_click(index)
        if self.opts.bfs:
            return self.board.tiles[index].BFS_open(), Counter.LEFT
        else:
            return self.board.tiles[index].open(), Counter.LEFT

    @operate
    def right(self, index):
        if not self.opts.nf:
            if self.opts.easy_flag:
                return self.board.tiles[index].flag(easy_flag=True), Counter.RIGHT
            else:
                return self.board.tiles[index].flag(), Counter.RIGHT
        else:
            return set(), Counter.OTHERS

    @operate
    def double(self, index):
        if not self.opts.nf:
            if self.opts.bfs:
                return self.board.tiles[index].BFS_double(), Counter.DOUBLE
            else:
                return self.board.tiles[index].double(), Counter.DOUBLE
        else:
            return set(), Counter.OTHERS

    @operate
    def left_hold(self, index):
        self.board.tiles[index].left_hold()
        return set(), Counter.OTHERS

    @operate
    def double_hold(self, index):
        if not self.opts.nf:
            self.board.tiles[index].double_hold()
        return set(), Counter.OTHERS

    def output(self, forced_whole_board = False):
        if self.stable and not forced_whole_board:
            return [(t.x, t.y, t.status) for t in self.recently_updated]
        else:
            return [(t.x, t.y, t.status) for t in self.board.tiles]

    # def __repr__(self):
    #     return '\n'.join(''.join(
    #         str(self.get_tile(x, y).status) for y in range(self.width))
    #                      for x in range(self.height)) + '\n'
