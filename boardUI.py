from core import Board

class BoardUI():
    def __init__(self):
        self.game = Board()

    def new_game(self):
        self.game = Board()

    def refresh(self):
        ...