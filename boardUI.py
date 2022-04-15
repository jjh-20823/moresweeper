"""The UI of the game."""

from settings import load_settings
from backend.game import Game
from resources import get_skin
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPainter, QMouseEvent

from time import monotonic_ns, perf_counter_ns

timer = perf_counter_ns
NS2MS = 1e-6


class boardUI(QtWidgets.QWidget):
    """The UI of the game."""

    left_hold = pyqtSignal(int, int)
    double_hold = pyqtSignal(int, int)
    left = pyqtSignal(int, int)
    right = pyqtSignal(int, int)
    double = pyqtSignal(int, int)
    # left_move = pyqtSignal(int, int)
    # double_move = pyqtSignal(int, int)
    drag = pyqtSignal(QMouseEvent)

    def __init__(self, parent=None):
        """Init the board UI."""
        super(boardUI, self).__init__(parent)
        self.setAttribute(Qt.WA_OpaquePaintEvent, True)
        self.signals = [
            self.left_hold, self.double_hold, self.left, self.right,
            self.double, self.drag
        ]
        self.setMouseTracking(True)
        self.init_board()

    def init_board(self):
        """Init the board."""
        self.settings = load_settings()

        self.game = Game(self.settings.game)
        self.height, self.width = self.game.board.height, self.game.board.width
        self.slots = [
            self.game.left_hold, self.game.double_hold, self.game.left,
            self.game.right, self.game.double, self.mousePressEvent
        ]

        self.tile_size = self.settings.ui.size
        self.tile_maps = get_skin(self.settings.ui.skin, self.settings.ui.size)

        self.doubled = False  # hold L, click R, then the release of L should be ignored

        for signal, slot in zip(self.signals, self.slots):
            try:
                signal.disconnect()
            except:
                pass
            signal.connect(slot)

    def paintEvent(self, event):
        """Paint the board."""
        super().paintEvent(event)
        painter = QPainter()
        painter.begin(self)
        # painter.setCompositionMode(QPainter.CompositionMode_ColorBurn)
        size = self.tile_size
        temp = self.game.board_output()
        for x, y, status in temp:
            painter.drawPixmap(x * size, y * size, self.tile_maps[status])
        painter.end()

    def resize(self, new_size):
        """Resize the board."""
        self.tile_maps = get_skin(self.opts["skin"], new_size)
        self.update()

    def mousePressEvent(self, event):
        """Handle mouse press event."""
        x_axis = event.localPos().x() / self.tile_size
        y_axis = event.localPos().y() / self.tile_size
        signal = int(event.buttons()) % 4
        if signal == 1 and not self.doubled:
            self.left_hold.emit(x_axis, y_axis)
        elif signal == 2:
            self.right.emit(x_axis, y_axis)
        elif signal == 3:
            self.double_hold.emit(x_axis, y_axis)

        if int(event.buttons()) == 4:
            self = self.game.init_upk()
            return
        self.update()

    def mouseReleaseEvent(self, event):
        """Handle mouse release event."""
        # a = timer()
        x_axis = event.localPos().x() / self.tile_size
        y_axis = event.localPos().y() / self.tile_size
        signal = int(event.buttons()) % 4
        if (signal == 1 and event.button() == Qt.RightButton) or (
                signal == 2 and event.button() == Qt.LeftButton):
            self.double.emit(x_axis, y_axis)
            self.doubled = True
        elif signal == 0:
            if event.button() == Qt.LeftButton and not self.doubled:
                self.left.emit(x_axis, y_axis)
            self.doubled = False
        self.update()
        # print((timer() - a)*NS2MS)

    def mouseMoveEvent(self, event):
        """Handle mouse move event."""
        signal = int(event.buttons()) % 4
        if signal != 2:
            self.drag.emit(event)

    def run(self):
        """Run the app."""
        self.setGeometry(135, 177, self.width * self.tile_size,
                         self.height * self.tile_size)
        self.show()
