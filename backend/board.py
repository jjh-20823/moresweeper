"""Board: A number of tiles."""

from .tile import Tile
from .stats import *
from random import shuffle


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

    def xy_index(self, x: int, y: int) -> int:
        """Convert a 2-D x-y coordinate to an 1-D index."""
        return x * self.width + y

    def tile_index(self, tile: Tile) -> int:
        """Get the index of the tile according to the current board."""
        return self.xy_index(tile.x, tile.y)

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
            [] for _ in range(self.height * self.width)
        ]
        self.op_is_counter = [0 for _ in range(self.tile_count)]

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

    def recover_tiles(self):
        """Recover all of the tiles to COVERED in a board."""
        for tile in self.tiles:
            tile.recover()
        self.init()

    def release(self):
        """Handle release event from upper layer."""
        for tile in self.tiles:
            tile.unhold()

    def is_finished(self) -> bool:
        """Check whether the board is finished completely."""
        for tile in self.tiles:
            if tile.covered and not tile.is_mine():
                return False
        return True

    def is_blasted(self) -> bool:
        """Check whether the board is blasted."""
        for tile in self.tiles:
            if not tile.covered and tile.is_mine():
                return True
        return False

    def is_ended(self):
        """Check whether the game is ended properly."""
        return self.is_finished() or self.is_blasted()

    def board_operate(func):
        """Decorator for board operations."""

        def inner(self, x: int, y: int, *args, replay: bool = False):
            """Wrapper of board_operate."""
            self.release()
            changed_tiles = set()
            if self.in_board(x, y):
                changed_tiles = func(self, self.xy_index(x, y), *args)
            if changed_tiles:
                self.calc_in_game_stats(changed_tiles, replay)
            if self.is_ended():
                if not replay:
                    self.calc_finish_stats()
            return changed_tiles

        return inner

    @board_operate
    def left(self, index: int, BFS: bool) -> set():
        """Handle left click event from upper layer."""
        return self.tiles[index].open(BFS)

    @board_operate
    def right(self, index: int, easy_flag: bool) -> set():
        """Handle right click event from upper layer."""
        return self.tiles[index].flag(easy_flag)

    @board_operate
    def double(self, index: int, BFS: bool) -> set():
        """Handle double click event from upper layer."""
        return self.tiles[index].double(BFS)

    @board_operate
    def left_hold(self, index) -> set():
        """Handle left hold event from upper layer."""
        self.tiles[index].left_hold()
        return set()

    @board_operate
    def double_hold(self, index) -> set():
        """Handle double hold event from upper layer."""
        self.tiles[index].double_hold()
        return set()

    def output(self):
        return [(t.x, t.y, t.status) for t in self.tiles]

    def neighbourhood(self, x, y):
        return self.get_tiles(
                ((x + i, y + j) for i in range(-2, 3)
                for j in range(-2, 3)))

    def calc_basic_stats(self):
        temp_tiles = self.tiles
        op_num, is_num = 1, -1
        for t in temp_tiles:
            if t.value == 0 and t.covered:
                op = t.open(BFS=False, test_op=True)
                for tt in op:
                    self.marker[self.tile_index(tt)].append(op_num)
                    self.op_is_counter[op_num] += 1
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
                    self.marker[self.tile_index(tt)].append(is_num)
                    self.op_is_counter[is_num] += 1
                is_num -= 1
        self.stats[STATS.IS] = -1 - is_num
        for tile in temp_tiles:
            tile.recover()

    def calc_in_game_stats(self, changed_tiles: set[Tile], replay):
        self.stats[STATS.flags] = sum(1 for t in self.tiles if t.flagged)
        self.stats[STATS.mines_left] = self.mines - self.stats[STATS.flags]
        if replay:
            for t in changed_tiles:
                if t.covered or t.is_mine():
                    continue
                else:
                    for temp_index in self.marker[self.tile_index(t)]:
                        self.op_is_counter[temp_index] -= 1
                        if temp_index < 0:
                            self.stats[STATS.solved_BBBV] += 1
                            if self.op_is_counter[temp_index] == 0:
                                self.stats[STATS.solved_IS] += 1
                        else:
                            if self.op_is_counter[temp_index] == 0:
                                self.stats[STATS.solved_OP] += 1
                                self.stats[STATS.solved_BBBV] += 1

    def calc_finish_stats(self):
        self.stats[STATS.flags] = sum(1 for t in self.tiles if t.flagged)
        self.stats[STATS.mines_left] = self.mines - self.stats[STATS.flags]
        self.stats[STATS.solved_BBBV], self.stats[STATS.solved_OP], self.stats[STATS.solved_IS] = 0, 0, 0
        for t in self.tiles:
            if t.covered or t.is_mine():
                continue
            else:
                for temp_index in self.marker[self.tile_index(t)]:
                    self.op_is_counter[temp_index] -= 1
                    if temp_index < 0:
                        self.stats[STATS.solved_BBBV] += 1
                        if self.op_is_counter[temp_index] == 0:
                            self.stats[STATS.solved_IS] += 1
                    else:
                        if self.op_is_counter[temp_index] == 0:
                            self.stats[STATS.solved_OP] += 1
                            self.stats[STATS.solved_BBBV] += 1

    def __repr__(self):
        return '\n'.join(''.join(
            str(self.get_tile(x, y).status) for y in range(self.width))
                         for x in range(self.height)) + '\n'
