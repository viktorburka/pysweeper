import sys
import random

from PySide2.QtWidgets import QApplication, QWidget, QFrame, QVBoxLayout
from PySide2.QtGui import QPalette, QColor
from playground import Playground


class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(220, 220, 220))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.header = QFrame()
        self.header.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.header.setFixedHeight(50)
        self.header.setLineWidth(4)
        self.header.setMidLineWidth(4)

        self.main = Playground()
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.setFixedSize(300, 360)
    widget.show()
    sys.exit(app.exec_())
