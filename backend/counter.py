"""The counter class."""


class Counter():
    """Counter: A number of game statistics."""

    def __init__(self):
        """Initialize the counter."""
        self.time = 0.0
        self.cl = {'l': 0, 'r': 0, 'd': 0}
        self.ce = {'l': 0, 'r': 0, 'd': 0}

    def start_timer(self):
        self.start_time = 0

    def add_cl(self, char):
        self.cl[char] += 1
