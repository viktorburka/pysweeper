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
    def __init__(self, controller):
        QFrame.__init__(self)
        self.game = controller
        self.mine_image = QPixmap("images/mine.png")
        self.mine_red_image = QPixmap("images/mine_red.png")
        self.cells = [[Cell() for x in range(CELL_COUNT)] for y in range(CELL_COUNT)]
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
        # due to imperfect bevel size there might be one pixel on and off
        # that causes the index go beyond the limit. we simply treat it as clicked on bevel
        if i == CELL_COUNT or j == CELL_COUNT:
            print("clicked on bevel")
            return
        cell = self.cells[i][j]
        # check if clicked on already opened cell
        if cell.open:
            return
        if cell.mine:
            cell.open = True
            cell.current = True
            print("boom!")
            self._open_all_mines()
            self.game.stop_game(False)
        else:
            # recursively open cells around current one
            self._open_cells_recursively(i, j)
            cell.open = True
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
                if cell.current:
                    painter.fillRect(rect, Qt.red)
                    painter.drawPixmap(rect.x() + x, rect.y() + y, self.mine_red_image)
                else:
                    painter.drawPixmap(rect.x() + x, rect.y() + y, self.mine_image)
            else:
                if cell.border != 0:
                    # draw number
                    font = painter.font()
                    font.setPixelSize(rect.height())
                    painter.setFont(font)
                    painter.setPen(Qt.blue)
                    painter.drawText(rect, Qt.AlignHCenter | Qt.AlignVCenter, str(cell.border))
        painter.setPen(Qt.black)
        painter.drawRect(rect.adjusted(0, 0, -1, -1))
        painter.restore()

    def _clicked_on_bevel(self, pos):
        bevel_width = self.lineWidth() + 2
        inside_hor_edge = pos.x() <= bevel_width or pos.x() >= self.width() - bevel_width
        inside_ver_edge = pos.y() <= bevel_width or pos.y() >= self.height() - bevel_width
        return inside_hor_edge or inside_ver_edge

    def _open_all_mines(self):
        for i in range(CELL_COUNT):
            for j in range(CELL_COUNT):
                if self.cells[i][j].mine:
                    self.cells[i][j].open = True

    def _open_cells_recursively(self, i, j):
        cell = self.cells[i][j]
        x = [-1, 0, 1, 1, 1, 0, -1, -1]
        y = [-1, -1, -1, 0, 1, 1, 1, 0]
        if not cell.open and not cell.mine:
            count = self._mines_around(i, j, CELL_COUNT)
            cell.open = True
            if count == 0:
                for m in range(len(x)):
                    adj_i = i + x[m]
                    adj_j = j + y[m]
                    if (adj_i < 0 or adj_i >= CELL_COUNT) or (adj_j < 0 or adj_j >= CELL_COUNT):
                        continue
                    self._open_cells_recursively(adj_i, adj_j)
            else:
                cell.border = count

    def _mines_around(self, i, j, boundary):
        x = [-1,  0,  1, 1, 1, 0, -1, -1]
        y = [-1, -1, -1, 0, 1, 1,  1,  0]
        count = 0
        for m in range(len(x)):
            adj_i = i + x[m]
            adj_j = j + y[m]
            if (adj_i < 0 or adj_i >= boundary) or (adj_j < 0 or adj_j >= boundary):
                continue
            if self.cells[adj_i][adj_j].mine:
                count += 1
        return count

    def reset(self):
        count = MINE_COUNT
        # reset all fields
        for i in range(CELL_COUNT):
            for j in range(CELL_COUNT):
                self.cells[i][j].open = False
                self.cells[i][j].mine = False
                self.cells[i][j].border = 0
        # populate mines
        while count > 0:
            i = random.randint(0, CELL_COUNT - 1)
            j = random.randint(0, CELL_COUNT - 1)
            if not self.cells[i][j].mine:
                self.cells[i][j].mine = True
                count -= 1
        self.update()
