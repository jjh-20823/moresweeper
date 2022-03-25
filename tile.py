from CONST import *

class Tile():
    # __slots__ = []
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_mine = False
        self.num = 0
        self.neighbours = set()

        self.flagged = False
        self.covered = True
        self.down = False

        self.status = COVERED # show what to draw
    
    def __repr__(self) -> str:
        return '({}, {})'.format(self.x, self.y)

    def set_mine(self):
        self.is_mine = True

    def set_num(self):
        if self.is_mine:
            return
        self.num = sum(1 for t in self.neighbours if t.is_mine)

    # update status
    def update(self):
        self.status = FLAGGED if self.flagged else DOWN if self.down else COVERED if self.covered else self.num
        return self.status

    # update status when finish
    def update_finish(self):
        if not self.flagged and self.is_mine:
            self.status = UNFLAGGED
        return self.status

    # update status when blast
    def update_blast(self):
        if self.flagged and not self.is_mine:
            self.status = WRONGFLAG
        elif not self.covered and self.is_mine:
            self.status = BLAST
        elif not self.flagged and self.is_mine:
            self.status = MINE
        return self.status

    def left_hold(self):
        if self.covered and not self.flagged:
            self.down = True

    def left_unhold(self):
        if self.covered and not self.flagged:
            self.down = False

    def double_hold(self):
        if not self.covered and not self.flagged:
            for t in self.neighbours:
                t.left_hold()

    def double_unhold(self):
        if not self.covered and not self.flagged:
            for t in self.neighbours:
                t.left_unhold()

    def basic_open(self):
        if self.flagged or not self.covered:
            return set()
        self.down = True
        self.covered = False
        if not self.is_mine and self.num == 0:
            return self.neighbours
        return set()

    def open(self):
        search = set(self)
        searched = set()
        while(search):
            t = search.pop()
            searched.add(t)
            search = search + t.basic_open() - searched
        return searched

    def double(self):
        if self.covered:
            self.down = False
            return set()
        temp = set()
        if self.num == sum(1 for t in self.neighbours if t.flagged):
            for t in self.neighbours:
                temp = temp + t.open()
        # return temp

    def basic_BFS_open(self):
        if self.flagged or not self.covered:
            return set()
        self.down = True
        self.covered = False
        if not self.is_mine and self.num == sum(1 for t in self.neighbours if t.flagged):
            return self.neighbours
        return set()

    def BFS_open(self):
        search = set(self)
        searched = set()
        while(search):
            t = search.pop()
            searched.add(t)
            search = search + t.basic_BFS_open() - searched
        return searched

    def BFS_double(self):
        if self.covered:
            self.down = False
            return set()
        temp = set()
        if self.num == sum(1 for t in self.neighbours if t.flagged):
            for t in self.neighbours:
                temp = temp + t.BFS_open()
        # return temp

    def flag(self):
        if self.flagged:
            self.flagged = False
        elif self.covered:
            self.flagged = True

    def easy_flag(self):
        if self.flagged:
            self.flagged = False
        elif self.covered:
            self.flagged = True
        elif self.num == sum(1 for t in self.neighbours if t.covered):
            for t in self.neighbours:
                t.flagged = True