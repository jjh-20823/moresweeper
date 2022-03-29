"""Main program of the minesweeper game."""

import sys
from PyQt5.QtWidgets import QApplication
from boardUI import boardUI


class Example(boardUI):
    """Main GUI."""

    def __init__(self):
        """Initialize the GUI."""
        super().__init__()
        self.setGeometry(300, 300, 960, 512)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
