"""Game: upper layer to communicate with UI and board."""

from .tile import Tile
from .counter import Counter
from .board import Board


class Game(object):
    """Game: upper layer to communicate with UI and board."""

    def __init__(self, settings: any):
        """Initialize a game."""
        self.opts: any = settings
        self.init()

    def init(self):
        """Initialize the board and counter."""
        self.board = Board(self.opts)
        self.first: bool = True
        self.win: bool = False
        self.lose: bool = False
        self.upk: bool = False
        self.stable: bool = False
        self.recently_updated: list[Tile] = self.board.tiles.copy()
        self.stats = self.board.stats
        self.counter: Counter = Counter(self.stats)

    def set_mines(self, x, y):
        """Set mines for the board."""
        if not self.upk:
            # don't need to update the mine field when it is UPK mode
            self.board.set_mines(x, y)
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
        self.stats = self.board.stats
        self.counter: Counter = Counter(self.stats)

    def start(self, x, y):
        """Start the game."""
        # while not self.valid_bv:
        self.set_mines(x, y)
        self.counter.start_timer()
        self.first = False

    def end(self):
        """End the game."""
        self.counter.stop_timer()
        if self.board.is_blasted():
            self.stable = False
            self.lose = True
            for tile in self.board.tiles:
                tile.update_blast()
        elif self.board.is_finished():
            self.stable = False
            self.win = True
            for tile in self.board.tiles:
                tile.update_finish()

    def operate(func):
        """Handle mouse event from upper layer."""

        def inner(self, x: float = -5.0, y: float = -5.0):
            if self.win or self.lose:
                return
            changed_tiles, button = func(self, int(x), int(y),
                                         replay=True)  # The real operation
            self.counter.refresh(changed_tiles, button)
            pending_tiles = changed_tiles | set(
                self.board.get_neighbours(x, y, radius=2, itself=True))
            # self.save_MouseTrack
            # ...
            # print(self.stats)
            if self.board.is_ended():
                self.end()
            else:
                self.stable = True
                for tile in pending_tiles:
                    tile.update()
                self.recently_updated = pending_tiles

        return inner

    @operate
    def left(self, x, y, **kwargs):
        """Handle left click."""
        if self.first:
            self.start(x, y)
        return self.board.left(x, y, self.opts.bfs, **kwargs), Counter.LEFT

    @operate
    def right(self, x, y, **kwargs):
        """Handle right click."""
        if not self.opts.nf:
            return self.board.right(x, y, self.opts.easy_flag,
                                    **kwargs), Counter.RIGHT
        else:
            return set(), Counter.OTHERS

    @operate
    def double(self, x, y, **kwargs):
        """Handle double click."""
        if not self.opts.nf:
            return self.board.double(x, y, self.opts.bfs,
                                     **kwargs), Counter.DOUBLE
        else:
            return set(), Counter.OTHERS

    @operate
    def left_hold(self, x, y, **kwargs):
        """Handle left click and holding."""
        return self.board.left_hold(x, y, **kwargs), Counter.OTHERS

    @operate
    def double_hold(self, x, y, **kwargs):
        """Handle double click and holding."""
        if not self.opts.nf:
            return self.board.double_hold(x, y, **kwargs), Counter.OTHERS
        return set(), Counter.OTHERS

    @operate
    def nothing(self, *args, **kwargs):
        """Regularly refresh the counter."""
        return set(), Counter.OTHERS

    def board_output(self, forced_whole_board=False):
        """Output the board."""
        if self.stable and not forced_whole_board:
            return [(t.x, t.y, t.status) for t in self.recently_updated]
        else:
            return self.board.output()

    def time_output(self):
        """Output the time."""
        pass

    def mines_left_output(self):
        """Output the mines left."""
        pass
