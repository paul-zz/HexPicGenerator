import os, sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from src.MainWindow import MainWindow
from src.SettingsManager import SettingsManager
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if __name__ == '__main__':
    # Initialize the application
    app = QApplication(sys.argv)

    # Load the settings
    settings_manager = SettingsManager("./settings.ini")
    settings = settings_manager.loadSettings()

    # Load the main window and show it
    mainWindow = MainWindow()
    mainWindow.applySettings(settings)
    mainWindow.show()
    
    # Execute the application
    sys.exit(app.exec_())
