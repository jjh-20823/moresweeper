"""
Backend for the minesweeper game.

This file focus on inner logic of minesweeper, and does not handle UI logics.
This file contains three classes:
- Tile: Minimum unit of minesweeper
- Board: A number of tiles
- Counter: A number of game statistics
"""


class Tile(object):
    """Tile: Minimum unit of minesweeper."""

    MINE = -1  # opcode: MINE, 15
    BLAST = -2  # opcode: BLAST, 14
    WRONGFLAG = -3  # opcode: WRONGFLAG, 13
    UNFLAGGED = -4  # opcode: UNFLAGGED, 12
    COVERED = 9  # opcode: COVERED, 9
    DOWN = 10  # opcode: DOWN, 10
    FLAGGED = 11  # opcode: FLAGGED, 11

    def __init__(self, x, y):
        """Initialize a tile."""
        self.x: int = x  # coordinate X
        self.y: int = y  # coordinate Y
        self.num: int = 0  # number
        self.is_mine: bool = False  # mine indicator
        self.flagged: bool = False  # flag indicator
        self.covered: bool = True  # cover indicator
        self.down: bool = False  # pressed indicator
        self.status: int = Tile.COVERED  # status for upper layer
        self.neighbours: set[Tile] = set()  # neighbours

    def __repr__(self) -> str:
        """Print a tile."""
        return '({}, {})'.format(self.x, self.y)

    def set_mine(self):
        """Set a tile with a mine."""
        self.is_mine = True

    def set_num(self):
        """Set a tile with a number."""
        if self.is_mine:
            return
        self.num = sum(1 for t in self.neighbours if t.is_mine)

    def update(self):
        """Update status of a tile."""
        self.status = Tile.FLAGGED if self.flagged else Tile.DOWN if self.down else Tile.COVERED if self.covered else self.num
        return self.status

    def update_finish(self):
        """Update status of a tile after finishing a game."""
        if not self.flagged and self.is_mine:
            self.status = Tile.UNFLAGGED
        return self.status

    def update_blast(self):
        """Update status of a tile after failing a game."""
        self.update()
        if self.flagged and not self.is_mine:
            self.status = Tile.WRONGFLAG
        elif not self.covered and self.is_mine:
            self.status = Tile.BLAST
        elif not self.flagged and self.is_mine:
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
        if not self.flagged:
            for t in self.neighbours:
                t.left_hold()

    def double_unhold(self):
        """Change status when unholding the left and right mouse key."""
        self.unhold()
        if not self.flagged:
            for t in self.neighbours:
                t.unhold()

    def basic_open(self):
        """Handle basic opening."""
        self.unhold()
        if self.flagged or not self.covered:
            return set()
        self.covered = False
        if not self.is_mine and self.num == 0:
            return self.neighbours
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
        self.double_unhold()
        if not self.covered and self.num == sum(
                1 for t in self.neighbours if t.flagged):
            for t in self.neighbours:
                t.open()

    def basic_BFS_open(self):
        """Handle basic open with BFS."""
        self.unhold()
        if self.flagged or not self.covered:
            return set()
        self.covered = False
        if not self.is_mine and self.num == sum(
                1 for t in self.neighbours if t.flagged):
            return self.neighbours
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
        self.double_unhold()
        if not self.covered and self.num == sum(
                1 for t in self.neighbours if t.flagged):
            for t in self.neighbours:
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
        elif self.num == sum(1 for t in self.neighbours if t.covered):
            for t in self.neighbours:
                if t.covered:
                    t.flagged = True


class Counter():
    """Counter: A number of game statistics."""

    def __init__(self):
        """Initialize the counter."""
        pass
