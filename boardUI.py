from options import load_options
from backend.board import Board
from resources import get_skin
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPainter, QMouseEvent


class boardUI(QtWidgets.QLabel):

    left_hold = pyqtSignal(int, int)
    double_hold = pyqtSignal(int, int)
    left = pyqtSignal(int, int)
    right = pyqtSignal(int, int)
    double = pyqtSignal(int, int)
    # left_move = pyqtSignal(int, int)
    # double_move = pyqtSignal(int, int)
    drag = pyqtSignal(QMouseEvent)

    def __init__(self, parent=None):
        super(boardUI, self).__init__(parent)
        self.signals = [self.left_hold, self.double_hold, self.left, self.right, self.double, self.drag]
        self.setMouseTracking(True)
        self.init_board()

    def init_board(self):
        self.board = Board(load_options("game_style"))
        self.height, self.width = self.board.height, self.board.width
        self.slots = [self.board.left_hold, self.board.double_hold, self.board.left, self.board.right, self.board.double, self.mousePressEvent]

        self.opts = load_options("UI")
        self.tile_size = self.opts["size"]
        self.tile_maps = get_skin(self.opts["skin"], self.opts["size"])

        self.doubled = False  # hold L, click R, then the release of L should be ignored

        for signal, slot in zip(self.signals, self.slots):
            try:
                signal.disconnect()
            except:
                pass
            signal.connect(slot)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter()
        painter.begin(self)
        size = self.tile_size
        temp = self.board.output()
        for x in range(self.height):
            for y in range(self.width):
                painter.drawPixmap(y * size, x * size,
                                   self.tile_maps[temp[x][y]])
        painter.end()

    def resize(self, new_size):
        self.tile_maps = get_skin(self.opts["skin"], new_size)
        # self.update()

    def mousePressEvent(self, event):
        y_axis, x_axis = event.localPos().x(
        ) // self.tile_size, event.localPos().y() // self.tile_size
        signal = int(event.buttons()) % 4
        if signal == 1:
            self.left_hold.emit(x_axis, y_axis)
        elif signal == 2:
            self.right.emit(x_axis, y_axis)
        elif signal == 3:
            self.double_hold.emit(x_axis, y_axis)
            
        if int(event.buttons()) == 4:
            self = self.board.init_upk()
            return
        self.update()

    def mouseReleaseEvent(self, event):
        y_axis, x_axis = event.localPos().x(
        ) // self.tile_size, event.localPos().y() // self.tile_size
        signal = int(event.buttons()) % 4
        if signal == 1 or signal == 2:
            self.double.emit(x_axis, y_axis)
            self.doubled = True
        elif signal == 0:
            if event.button() == Qt.LeftButton and not self.doubled:
                self.left.emit(x_axis, y_axis)
            self.doubled = False
        self.update()

    def mouseMoveEvent(self, event):
        signal = int(event.buttons()) % 4
        if signal != 2:
            self.drag.emit(event)