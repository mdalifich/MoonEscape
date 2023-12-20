from PyQt5 import QtGui, QtCore
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

import sys


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Windows/MenuWindow.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.show()
    sys.exit(app.exec())
