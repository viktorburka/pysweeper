from PySide2.QtCore import QObject, Signal


class GameController(QObject):

    gameOver = Signal(bool)

    def __init__(self):
        QObject.__init__(self)

    def stop_game(self, win):
        self.gameOver.emit(win)
