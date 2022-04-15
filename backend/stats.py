"""A class for counting the game statistics."""

stats_count = 18
class STATS():
    """A class for counting the game statistics."""

    [
        mode, time, BBBV, OP, IS, 
        solved_BBBV, solved_OP, solved_IS, 
        flags, mines_left, 
        total_ce, left_ce, right_ce, double_ce, 
        total_cl, left_cl, right_cl, double_cl, 
    ] = (list(range(stats_count)))
