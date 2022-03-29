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
        self.value = -1

    def is_mine(self) -> bool:
        """Judge whether the tile is a mine by its value."""
        return self.value == Tile.MINE

    def set_value(self):
        """Set a tile with a value."""
        if self.is_mine():
            return

        # calculate the value of a tile
        value = 0
        for t in self.get_neighbours():
            value += (t.is_mine())
        self.value = value

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
        self.status = Tile.FLAGGED if self.flagged else Tile.DOWN if self.down else Tile.COVERED if self.covered else self.value
        return self.status

    def update_finish(self):
        """Update status of a tile after finishing a game."""
        self.update()
        if not self.flagged and self.is_mine():
            self.status = Tile.UNFLAGGED
        return self.status

    def update_blast(self):
        """Update status of a tile after failing a game."""
        self.update()
        if self.flagged and not self.is_mine():
            self.status = Tile.WRONGFLAG
        elif not self.covered and self.is_mine():
            self.status = Tile.BLAST
        elif not self.flagged and self.is_mine():
            self.status = Tile.MINE
        return self.status

    def left_hold(self):
        """Change status when holding the left mouse key."""
        if self.covered and not self.flagged:
            self.down = True

    def unhold(self):
        """Change status when unholding a single mouse key."""
        if not self.flagged:
            self.down = False

    def double_hold(self):
        """Change status when holding the left and right mouse key."""
        self.left_hold()
        for t in self.get_neighbours():
            t.left_hold()

    def basic_open(self):
        """Handle basic opening."""
        if self.flagged or not self.covered:
            return set()
        self.covered = False
        if not self.is_mine() and self.value == 0:
            return self.get_neighbours()
        return set()

    def open(self):
        """Handle normal opening."""
        search = set((self, ))
        searched = set()
        while (search):
            t = search.pop()
            searched.add(t)
            search = search | t.basic_open() - searched
        return searched

    def double(self):
        """Handle chording."""
        if not self.covered and self.value == sum(
                1 for t in self.get_neighbours() if t.flagged):
            for t in self.get_neighbours():
                t.open()

    def basic_BFS_open(self):
        """Handle basic open with BFS."""
        if self.flagged or not self.covered:
            return set()
        self.covered = False
        if not self.is_mine() and (self.value == sum(
                1 for t in self.get_neighbours() if t.flagged)
                                   or self.value == 0):
            return self.get_neighbours()
        return set()

    def BFS_open(self):
        """Handle normal open with BFS."""
        search = set((self, ))
        searched = set()
        while (search):
            t = search.pop()
            searched.add(t)
            search = search | t.basic_BFS_open() - searched
        return searched

    def BFS_double(self):
        """Handle chording with BFS."""
        if not self.covered and self.value == sum(
                1 for t in self.get_neighbours() if t.flagged):
            for t in self.get_neighbours():
                t.BFS_open()

    def flag(self):
        """Handle flagging."""
        if self.flagged:
            self.flagged = False
        elif self.covered:
            self.flagged = True

    def easy_flag(self):
        """Handle easy flagging."""
        if self.flagged:
            self.flagged = False
        elif self.covered:
            self.flagged = True
        elif self.value == sum(1 for t in self.get_neighbours() if t.covered):
            for t in self.get_neighbours():
                if t.covered:
                    t.flagged = True