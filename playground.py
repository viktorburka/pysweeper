import random

from PySide2.QtWidgets import QFrame
from PySide2.QtGui import QPainter, QPixmap
from PySide2.QtCore import Qt, QRect, QPoint

from cell import Cell

CELL_COUNT = 9
MINE_COUNT = 10
# MINE_COUNT = 60
CELL_SIZE = 30


class Playground(QFrame):
    def __init__(self):
        QFrame.__init__(self)
        self.mine_image = QPixmap("images/mine.png")
        self.reset()

    def paintEvent(self, paintEvent):
        # let QFrame to draw its background first
        QFrame.paintEvent(self, paintEvent)
        # init painter to start drawing on current widget surface
        painter = QPainter(self)
        # translate is mandatory since frame has a bevel
        painter.translate(self.lineWidth(), self.lineWidth())
        # render cells
        for i in range(CELL_COUNT):
            for j in range(CELL_COUNT):
                rect = QRect(i*CELL_SIZE, j*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                self._draw_cell(painter, rect, self.cells[i][j])

    def mousePressEvent(self, mouseEvent):
        # first check whether the click position is on
        # the bevel and not a cell and ignore it in that case
        if self._clicked_on_bevel(mouseEvent.pos()):
            print("clicked on bevel")
            return
        # adjust position by bevel size
        pos = mouseEvent.pos() - QPoint(self.lineWidth(), self.lineWidth())
        i = pos.x() // CELL_SIZE
        j = pos.y() // CELL_SIZE
        print("pos = {}".format(pos))
        print("i = {}, j = {}".format(i, j))
        # due to imperfect bevel size there might be one pixel on and off
        # that causes the index go beyond the limit. we simply treat it as clicked on bevel
        if i == CELL_COUNT or j == CELL_COUNT:
            print("clicked on bevel")
            return
        cell = self.cells[i][j]
        cell.open = True
        if cell.mine:
            print("boom!")
        # call parent widget mouse click method
        QFrame.mousePressEvent(self, mouseEvent)
        # repaint the widget
        self.update()

    def _draw_cell(self, painter, rect, cell):
        painter.save()
        if not cell.open:
            painter.fillRect(rect, Qt.gray)
        else:
            painter.fillRect(rect, Qt.lightGray)
            if cell.mine:
                sz = (rect.size() - self.mine_image.size())
                x = sz.width() // 2
                y = sz.height() // 2
                painter.drawPixmap(rect.x() + x, rect.y() + y, self.mine_image)
        painter.setPen(Qt.black)
        painter.drawRect(rect.adjusted(0, 0, -1, -1))
        painter.restore()

    def _clicked_on_bevel(self, pos):
        bevel_width = self.lineWidth() + 2
        inside_hor_edge = pos.x() <= bevel_width or pos.x() >= self.width() - bevel_width
        inside_ver_edge = pos.y() <= bevel_width or pos.y() >= self.height() - bevel_width
        return inside_hor_edge or inside_ver_edge

    def reset(self):
        self.cells = [[Cell() for x in range(CELL_COUNT)] for y in range(CELL_COUNT)]
        count = MINE_COUNT
        while count > 0:
            i = random.randint(0, CELL_COUNT - 1)
            j = random.randint(0, CELL_COUNT - 1)
            if not self.cells[i][j].mine:
                self.cells[i][j].mine = True
                count -= 1
        # for i in range(CELL_COUNT):
        #     for j in range(CELL_COUNT):
        #         print(self.cells[i][j].open, end=" ")
        #     print()

