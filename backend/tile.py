"""The tile class."""


class Tile(object):
    """Tile: Minimum unit of minesweeper."""

    MINE = -1  # opcode: MINE, 15
    BLAST = -2  # opcode: BLAST, 14
    WRONGFLAG = -3  # opcode: WRONGFLAG, 13
    UNFLAGGED = -4  # opcode: UNFLAGGED, 12
    COVERED = 9  # opcode: COVERED, 9
    DOWN = 10  # opcode: DOWN, 10
    FLAGGED = 11  # opcode: FLAGGED, 11

    def __init__(self, x: int, y: int):
        """Initialize a tile."""
        self.x: int = x  # coordinate X
        self.y: int = y  # coordinate Y
        self.value: int = 0  # value: -1 for mines, 0-8 for numbers
        self.flagged: bool = False  # flag indicator
        self.covered: bool = True  # cover indicator
        self.down: bool = False  # pressed indicator
        self.status: int = Tile.COVERED  # status for upper layer
        self.neighbours: set[Tile] = set()  # neighbours

    def __repr__(self) -> str:
        """Print a tile."""
        return f'Tile[v: {self.value}]: (x: {self.x}, y: {self.y})'

    def set_mine(self):
        """Set a tile with a mine."""
        self.value = Tile.MINE

        # set the value of a mine's neighbour
        # this will simplify board construction process
        for t in self.get_neighbours():
            if not t.is_mine():
                t.value += 1  # update a neighbour's value

    def is_mine(self) -> bool:
        """Judge whether the tile is a mine by its value."""
        return self.value == Tile.MINE

    def recover(self):
        """Recover the status of the tile."""
        self.flagged = False  # flag indicator
        self.covered = True  # cover indicator
        self.down = False  # pressed indicator
        self.status = Tile.COVERED  # status for upper layer

    def get_neighbours(self) -> set:
        """Get the neighbours of a tile."""
        return self.neighbours

    def update(self):
        """Update status of a tile."""
        if self.flagged:
            self.status = Tile.FLAGGED
        elif self.down:
            self.status = Tile.DOWN
        elif self.covered:
            self.status = Tile.COVERED
        else:
            self.status = self.value

    def update_finish(self):
        """Update status of a tile after finishing a game."""
        self.update()
        if not self.flagged and self.is_mine():
            self.status = Tile.UNFLAGGED

    def update_blast(self):
        """Update status of a tile after failing a game."""
        self.update()
        if self.flagged and not self.is_mine():
            self.status = Tile.WRONGFLAG
        elif not self.covered and self.is_mine():
            self.status = Tile.BLAST
        elif not self.flagged and self.is_mine():
            self.status = Tile.MINE

    def left_hold(self):
        """Change status when holding the left mouse key."""
        if self.covered and not self.flagged:
            self.down = True

    def double_hold(self):
        """Change status when holding the left and right mouse key."""
        self.left_hold()
        for t in self.get_neighbours():
            t.left_hold()

    def unhold(self):
        """Change status when unholding a single mouse key."""
        if not self.flagged:
            self.down = False

    def basic_open(self, BFS: bool = False):
        """Handle basic opening."""
        if self.flagged or not self.covered:
            return set()
        self.covered = False
        if not self.is_mine() and (
                self.value == 0 or (BFS and self.value == sum(
                    1 for t in self.get_neighbours() if t.flagged))):
            return self.get_neighbours() | set((self, ))
        return set((self, ))

    def open(self, BFS: bool = False, test_op: bool = False):
        """Handle normal opening."""
        search = set((self, ))
        searched = set()
        changed = set()
        while (search):
            t = search.pop()
            searched.add(t)
            temp = t.basic_open(BFS)
            if temp:
                search = search | temp - searched
                changed.add(t)
        return changed if not test_op else searched

    def double(self, BFS: bool = False):
        """Handle chording."""
        if not self.covered and self.value == sum(
                1 for t in self.get_neighbours() if t.flagged):
            return set.union(*(t.open(BFS) for t in self.get_neighbours()))
        return set()

    def flag(self, easy_flag: bool = False):
        """Handle flagging and easy flagging."""
        if self.flagged:
            self.flagged = False
            return set((self, ))
        elif self.covered:
            self.flagged = True
            return set((self, ))
        elif easy_flag:
            covered_neighbours = set(t for t in self.get_neighbours()
                                     if t.covered)
            unflagged_neighbours = set(t for t in self.get_neighbours()
                                       if t.covered and not t.flagged)
            if self.value == len(covered_neighbours):
                for t in covered_neighbours:
                    t.flagged = True
                return unflagged_neighbours
        return set()
