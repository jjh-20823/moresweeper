"""The counter class."""
from time import monotonic_ns, perf_counter_ns
from .stats import STATS
timer = perf_counter_ns # Not sure which clock to use
NS2S = 1e-9

class Counter():
    """Counter: A number of game statistics."""

    LEFT = 1
    RIGHT = 2
    DOUBLE = 3
    OTHERS = 0

    def __init__(self, stats):
        """Initialize the counter."""
        self.start_ns_time = 0
        self.game_time = -1.0
        self.active = False
        self.stats = stats

    def refresh_timer(self):
        """Refresh the game's timer."""
        if self.active:
            self.game_time = (timer() - self.start_ns_time) * NS2S

    def get_time(self):
        """Get the game elapsed time."""
        return max(self.game_time, 0.0)

    def start_timer(self):
        """Start the timer."""
        self.start_ns_time = timer()
        self.active = True
        self.refresh_timer()

    def stop_timer(self):
        """Stop the timer."""
        self.refresh_timer()
        self.active = False

    def refresh(self, changed_tiles=set(), button=OTHERS):
        """Update statistics of ce(effective clicks) and cl(clicks)."""
        if self.active:
            if button != Counter.OTHERS:
                self.stats[STATS.total_cl] += 1
                self.stats[STATS.total_cl + button] += 1
                if changed_tiles:
                    self.stats[STATS.total_ce] += 1
                    self.stats[STATS.total_ce + button] += 1
            self.refresh_timer()
                # do some calculate