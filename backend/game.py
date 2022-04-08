"""Board: A number of tiles."""

from telnetlib import PRAGMA_HEARTBEAT
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
        self.win: bool = False
        self.lose: bool = False
        self.upk: bool = False
        self.stable: bool = False
        self.recently_updated: list[Tile] = self.board.tiles.copy()
        # self.holding: set(Tile) = set()
        # self.counter: Counter = Counter()

    def set_mines(self, x, y):
        """Set mines for the board."""
        if not self.upk:
            self.board.set_mines(x, y)  # don't need to update the mine field when it is UPK mode
        self.board.calc_basic_stats()
        
    def init_upk(self):
        """Toggle UPK mode."""
        self.board.recover_tiles()
        self.first = True
        self.win = False
        self.lose = False
        self.upk = True
        self.stable = False
        self.recently_updated = self.board.tiles.copy()

    def start(self, x, y):
        self.set_mines(x, y)
        # self.counter.start_timer()
        self.first = False

    def end(self):
        if self.board.blast:
            self.stable = False
            self.lose = True
            for tile in self.board.tiles:
                tile.update_blast()
        elif self.board.finish:
            self.stable = False
            self.win = True
            for tile in self.board.tiles:
                tile.update_finish()

    def operate(func):

        def inner(self, x: float, y: float):
            if self.win or self.lose:
                return
            changed_tiles, button = func(self, int(x), int(y), replay=True) # The real operation
            # self.update_Counter
            # self.save_MouseTrack
            # ...
            if self.board.blast or self.board.finish:
                self.end()
            else:
                self.stable = True
                for tile in changed_tiles:
                    tile.update()
                self.recently_updated = changed_tiles

        return inner

    @operate
    def left(self, x, y, **kwargs):
        if self.first:
            self.start(x, y)
        return self.board.left(x, y, self.opts.bfs, **kwargs), Counter.LEFT

    @operate
    def right(self, x, y, **kwargs):
        if not self.opts.nf:
            return self.board.right(x, y, self.opts.easy_flag, **kwargs), Counter.RIGHT
        else:
            return set(), Counter.OTHERS

    @operate
    def double(self, x, y, **kwargs):
        if not self.opts.nf:
            return self.board.double(x, y, self.opts.bfs, **kwargs), Counter.DOUBLE
        else:
            return set(), Counter.OTHERS

    @operate
    def left_hold(self, x, y, **kwargs):
        return self.board.left_hold(x, y, **kwargs), Counter.OTHERS

    @operate
    def double_hold(self, x, y, **kwargs):
        if not self.opts.nf:
            return self.board.double_hold(x, y, **kwargs), Counter.OTHERS
        return set(), Counter.OTHERS

    def board_output(self, forced_whole_board = False):
        if self.stable and not forced_whole_board:
            return [(t.x, t.y, t.status) for t in self.recently_updated]
        else:
            return self.board.output()

    # def __repr__(self):
    #     return '\n'.join(''.join(
    #         str(self.get_tile(x, y).status) for y in range(self.width))
    #                      for x in range(self.height)) + '\n'
