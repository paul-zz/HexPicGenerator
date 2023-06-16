import os, sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from src.MainWindow import MainWindow

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()
    
    sys.exit(app.exec_())
