"""The counter class."""
from time import monotonic_ns, perf_counter_ns
timer = perf_counter_ns # Not sure which clock to use
NS2S = 1e-9

class Counter():
    """Counter: A number of game statistics."""
    LEFT = 'l'
    RIGHT = 'r'
    DOUBLE = 'd'
    OTHERS = 'o'

    def __init__(self):
        """Initialize the counter."""
        self.start_time = 0
        self.end_time = 0
        self.game_time = 0
        self.cl = {Counter.LEFT: 0, Counter.RIGHT: 0, Counter.DOUBLE: 0}
        self.ce = {Counter.LEFT: 0, Counter.RIGHT: 0, Counter.DOUBLE: 0}

    def update_ce_cl(self, result, button):
        """Update statistics of ce(effective clicks) and cl(clicks)."""
        if button == Counter.OTHERS:
            return
        self.cl[button] += 1
        if result:
            self.ce[button] += 1

    def start_timer(self):
        """Start the timer."""
        self.start_time = timer()
        self.end_time = self.start_time()

    def refresh_timer(self):
        self.game_time = (timer() - self.start_time) * NS2S
