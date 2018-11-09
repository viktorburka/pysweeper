from PySide2.QtWidgets import QFrame
from PySide2.QtGui import QPainter, QPixmap
from PySide2.QtCore import Qt, QRect, QPoint

from game_controller import GameController


class Playground(QFrame):
    def __init__(self, controller):
        QFrame.__init__(self)
        self.game = controller
        self.mine_image = QPixmap("images/mine.png")
        self.mine_red_image = QPixmap("images/mine_red.png")
        self.flag_image = QPixmap("images/flag.png")
        self.cell_raised_image = QPixmap("images/cell_raised.png")

        controller.gameReset.connect(self.repaint)
        self.reset()

    def paintEvent(self, paintEvent):
        # let QFrame to draw its background first
        QFrame.paintEvent(self, paintEvent)
        # init painter to start drawing on current widget surface
        painter = QPainter(self)
        # translate is mandatory since frame has a bevel
        painter.translate(self.lineWidth(), self.lineWidth())
        # render cells
        for i in range(GameController.CELL_COUNT):
            for j in range(GameController.CELL_COUNT):
                cell_size = GameController.CELL_SIZE
                rect = QRect(i*cell_size, j*cell_size, cell_size, cell_size)
                self._draw_cell(painter, rect, self.game.cells[i][j])

    def mousePressEvent(self, mouseEvent):
        # first check whether the click position is on
        # the bevel and not a cell and ignore it in that case
        if self._clicked_on_bevel(mouseEvent.pos()):
            print("clicked on bevel")
            return
        # adjust position by bevel size
        pos = mouseEvent.pos() - QPoint(self.lineWidth(), self.lineWidth())
        i = pos.x() // GameController.CELL_SIZE
        j = pos.y() // GameController.CELL_SIZE
        # due to imperfect bevel size there might be one pixel on and off
        # that causes the index go beyond the limit. we simply treat it as clicked on bevel
        if i == GameController.CELL_COUNT or j == GameController.CELL_COUNT:
            print("clicked on bevel")
            return
        cell = self.game.cells[i][j]
        # check if clicked on already opened cell
        if cell.open:
            return
        if mouseEvent.button() == Qt.LeftButton:
            if not cell.flag:  # if flag is set, don't do anything
                if cell.mine:
                    cell.open = True
                    cell.current = True
                    print("boom!")
                    self._open_all_mines()
                    self.game.stop_game(False)
                else:
                    # recursively open cells around current one
                    self.game.open_cells_recursively(i, j)
                    cell.open = True
        else:
            if not cell.open:
                if cell.flag:  # if flag already set, remote it
                    cell.flag = False
                    self.game.set_flags_count(self.game.flags + 1)
                else:  # otherwise set the flag
                    if self.game.flags > 0:
                        cell.flag = True
                        self.game.set_flags_count(self.game.flags - 1)
        # call parent widget mouse click method
        QFrame.mousePressEvent(self, mouseEvent)
        # repaint the widget
        self.update()

    def _draw_cell(self, painter, rect, cell):
        painter.save()
        if not cell.open:
            painter.drawPixmap(rect.x(), rect.y(), self.cell_raised_image)
            if cell.flag:
                sz = (rect.size() - self.flag_image.size())
                x = sz.width() // 2
                y = sz.height() // 2
                painter.drawPixmap(rect.x() + x, rect.y() + y, self.flag_image)
            painter.setPen(Qt.black)
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
            painter.setPen(Qt.gray)
        painter.drawRect(rect.adjusted(0, 0, -1, -1))
        painter.restore()

    def _clicked_on_bevel(self, pos):
        bevel_width = self.lineWidth() + 2
        inside_hor_edge = pos.x() <= bevel_width or pos.x() >= self.width() - bevel_width
        inside_ver_edge = pos.y() <= bevel_width or pos.y() >= self.height() - bevel_width
        return inside_hor_edge or inside_ver_edge

    def _open_all_mines(self):
        for i in range(GameController.CELL_COUNT):
            for j in range(GameController.CELL_COUNT):
                if self.game.cells[i][j].mine:
                    self.game.cells[i][j].open = True

    def reset(self):
        self.game.restart_game()
