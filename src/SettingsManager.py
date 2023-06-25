from PyQt5.QtCore import QSettings, QFile, QTextCodec

class SettingsManager:
    def __init__(self, settings_dir):
        self.settings_dir = settings_dir
        self.settings_obj = QSettings(settings_dir, QSettings.IniFormat)
        self.settings_obj.setIniCodec(QTextCodec.codecForName("UTF-8"))

    def loadSettings(self):
        if not QFile.exists(self.settings_dir):
            self.generateDefaultSettings()
        return self.settings_obj

    def generateDefaultSettings(self):
        self.settings_obj.setValue("reverse", False)
        self.settings_obj.setValue("line_break", 16)
        self.settings_obj.setValue("separator", ", ")
        self.settings_obj.setValue("front_string", "")
        self.settings_obj.setValue("end_string", "")
        self.settings_obj.sync()
