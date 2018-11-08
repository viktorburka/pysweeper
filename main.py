import sys

from PySide2.QtWidgets import QApplication, QWidget, QFrame, QVBoxLayout, QMessageBox
from PySide2.QtGui import QPalette, QColor
from playground import Playground
from game_controller import GameController


class PySweeperWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        controller = GameController()
        controller.gameOver.connect(self.game_over)

        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(220, 220, 220))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.header = QFrame()
        self.header.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.header.setFixedHeight(50)
        self.header.setLineWidth(4)
        self.header.setMidLineWidth(4)

        self.main = Playground(controller)
        self.main.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.main.setFixedHeight(280)
        self.main.setLineWidth(4)
        self.main.setMidLineWidth(4)

        self.layout = QVBoxLayout()
        self.layout.setMargin(10)
        self.layout.setSpacing(5)
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.main)
        self.setLayout(self.layout)

    def game_over(self, result):
        print("result: {}".format(result))
        msg = "Congratulations. You won!" if result else "Sorry you lost."
        question = "{} Would you like to play again?".format(msg)
        answer = QMessageBox().question(self, 'Game Over', question, QMessageBox.Yes, QMessageBox.No)
        if answer == QMessageBox.Yes:
            self.main.reset()
        else:
            app.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = PySweeperWidget()
    widget.setFixedSize(300, 360)
    widget.show()
    sys.exit(app.exec_())
