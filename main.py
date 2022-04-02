"""Main program of the minesweeper game."""

import sys
from PyQt5.QtWidgets import QApplication
from boardUI import boardUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = boardUI()
    main.run()
    sys.exit(app.exec_())
