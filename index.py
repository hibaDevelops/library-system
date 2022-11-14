from qtpy.QtCore import *
from qtpy.QtGui import *
from PyQt5.QtWidgets import *
import sys

from qtpy.uic import loadUiType

ui,_ = loadUiType('Library UI.ui')


class MainApp(QMainWindow, ui):
    def __int__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
