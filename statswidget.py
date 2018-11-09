from PySide2.QtWidgets import QFrame
from PySide2.QtWidgets import QHBoxLayout
from PySide2.QtWidgets import QLabel
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QSpacerItem
from PySide2.QtWidgets import QSizePolicy
from PySide2.QtGui import QPalette
from PySide2.QtCore import Qt


class StatsWidget(QFrame):
    def __init__(self, controller):
        QFrame.__init__(self)

        self.flags = QLabel("0")
        self.flags.setFixedWidth(50)
        self.flags.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.flags.setAutoFillBackground(True)

        flagsFont = self.flags.font()
        flagsFont.setPixelSize(28)
        self.flags.setFont(flagsFont)

        flagsPalette = self.flags.palette()
        flagsPalette.setColor(QPalette.Foreground, Qt.red)
        flagsPalette.setColor(QPalette.Window, Qt.black)
        self.flags.setPalette(flagsPalette)

        self.reset = QPushButton()
        self.reset.setFixedSize(45, 45)

        self.seconds = QLabel("0")
        self.seconds.setFixedWidth(50)
        self.seconds.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.seconds.setAutoFillBackground(True)

        secondsFont = self.seconds.font()
        secondsFont.setPixelSize(28)
        self.seconds.setFont(secondsFont)

        secondsPalette = self.seconds.palette()
        secondsPalette.setColor(QPalette.Foreground, Qt.red)
        secondsPalette.setColor(QPalette.Window, Qt.black)
        self.seconds.setPalette(secondsPalette)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(5, 0, 5, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.flags)
        self.layout.addSpacerItem(QSpacerItem(100, 10, QSizePolicy.Maximum))
        self.layout.addWidget(self.reset)
        self.layout.addSpacerItem(QSpacerItem(100, 10, QSizePolicy.Maximum))
        self.layout.addWidget(self.seconds)
        self.setLayout(self.layout)

