from PySide2.QtWidgets import QFrame
from PySide2.QtGui import QPainter
from PySide2.QtCore import Qt, QRect

CELL_COUNT = 9
CELL_SIZE = 30


class Playground(QFrame):
    def __init__(self):
        QFrame.__init__(self)

    def paintEvent(self, *args, **kwargs):
        # let QFrame to draw its background first
        QFrame.paintEvent(self, *args)
        # init painter to start drawing on current widget surface
        painter = QPainter(self)
        # translate is mandatory since frame has a bevel
        painter.translate(self.lineWidth(), self.lineWidth())
        # render cells
        for i in range(CELL_COUNT):
            for j in range(CELL_COUNT):
                rect = QRect(i*CELL_SIZE, j*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                self._draw_cell(painter, rect)

    def _draw_cell(self, painter, rect):
        painter.save()
        painter.fillRect(rect, Qt.red)
        painter.setPen(Qt.black)
        painter.drawRect(rect.adjusted(0, 0, -1, -1))
        painter.restore()

    def hello(self):
        print("hello")
