"""The counter class."""


class Counter():
    """Counter: A number of game statistics."""
    LEFT = 'l'
    RIGHT = 'r'
    DOUBLE = 'd'
    OTHERS = 'o'

    def __init__(self):
        """Initialize the counter."""
        self.time = 0.0
        self.cl = {Counter.LEFT: 0, Counter.RIGHT: 0, Counter.DOUBLE: 0}
        self.ce = {Counter.LEFT: 0, Counter.RIGHT: 0, Counter.DOUBLE: 0}

    def start_timer(self):
        """Start the timer."""
        self.start_time = 0

    def update_ce_cl(self, result, button):
        """Update statistics of ce(effective clicks) and cl(clicks)."""
        if button == Counter.OTHERS:
            return
        self.cl[button] += 1
        if result:
            self.ce[button] += 1
