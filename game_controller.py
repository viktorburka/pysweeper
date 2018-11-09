import random

from PySide2.QtCore import QObject, Signal

from cell import Cell


class GameController(QObject):
    CELL_COUNT = 9
    MINE_COUNT = 10
    # MINE_COUNT = 60
    CELL_SIZE = 30

    gameOver = Signal(bool)
    gameReset = Signal()
    flagsCountChanged = Signal(int)

    def __init__(self):
        QObject.__init__(self)
        self.cells = [[Cell() for x in range(self.CELL_COUNT)] for y in range(self.CELL_COUNT)]
        self.flags = self.MINE_COUNT
        self.reset()

    def restart_game(self):
        self.reset()
        self.gameReset.emit()

    def set_flags_count(self, count):
        self.flags = count
        self.flagsCountChanged.emit(self.flags)

    def open_cells_recursively(self, i, j):
        cell = self.cells[i][j]
        x = [-1, 0, 1, 1, 1, 0, -1, -1]
        y = [-1, -1, -1, 0, 1, 1, 1, 0]
        if not cell.open and not cell.mine:
            count = self.mines_around(i, j, self.CELL_COUNT)
            cell.open = True
            if count == 0:
                for m in range(len(x)):
                    adj_i = i + x[m]
                    adj_j = j + y[m]
                    out_to_left = adj_i < 0 or adj_i >= self.CELL_COUNT
                    out_to_right = adj_j < 0 or adj_j >= self.CELL_COUNT
                    if out_to_left or out_to_right:
                        continue
                    self.open_cells_recursively(adj_i, adj_j)
            else:
                cell.border = count

    def mines_around(self, i, j, boundary):
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
        self.set_flags_count(self.MINE_COUNT)
        count = self.MINE_COUNT
        # reset all fields
        for i in range(self.CELL_COUNT):
            for j in range(self.CELL_COUNT):
                self.cells[i][j].reset()
        # populate mines
        while count > 0:
            i = random.randint(0, self.CELL_COUNT - 1)
            j = random.randint(0, self.CELL_COUNT - 1)
            if not self.cells[i][j].mine:
                self.cells[i][j].mine = True
                count -= 1

    def stop_game(self, win):
        self.gameOver.emit(win)
