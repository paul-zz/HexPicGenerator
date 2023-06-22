import sys

from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtWidgets import (QDialog,
                             QDialogButtonBox,
                             QSpinBox,
                             QLineEdit,
                             QVBoxLayout,
                             QFormLayout,
                             QApplication
)


class SettingWindow(QDialog):
    def __init__(self, parent = None, settings_obj = None):
        super().__init__()

        # Vars
        self.settings_obj = None

        # UI
        self.setWindowTitle("Settings")
        self.setFixedWidth(500)
        
        # Setting area
        self.layout_settings = QFormLayout()
        self.label_line_break = "单行数目："
        self.label_separator = "分隔符："
        self.label_front_str = "前缀文本："
        self.label_end_str = "后缀文本："
        self.spinbox_line_break = QSpinBox()
        self.textedit_separator = QLineEdit()
        self.textedit_front_str = QLineEdit()
        self.textedit_end_str = QLineEdit()

        self.spinbox_line_break.setToolTip("一行显示的项目数")
        self.textedit_separator.setToolTip("输出结果的分隔符，如', '")
        self.textedit_front_str.setToolTip("输出结果的前缀，如'const unsigned char bitmap[]={'")
        self.textedit_end_str.setToolTip("输出后缀的后缀，如'};'")

        self.layout_settings.addRow(self.label_line_break, self.spinbox_line_break)
        self.layout_settings.addRow(self.label_separator, self.textedit_separator)
        self.layout_settings.addRow(self.label_front_str, self.textedit_front_str)
        self.layout_settings.addRow(self.label_end_str, self.textedit_end_str)

        # Dialog Buttons
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        vbox = QVBoxLayout()
        vbox.addLayout(self.layout_settings)
        vbox.addWidget(self.buttonBox)

        self.setLayout(vbox)
        self.readSettings(settings_obj)

    def readSettings(self, settings_obj : QSettings):
        # Receive a QSettings object and apply
        self.settings_obj = settings_obj
        line_break = int(settings_obj.value("line_break"))
        separator = settings_obj.value("separator")
        front_string = settings_obj.value("front_string")
        end_string = settings_obj.value("end_string")
        self.spinbox_line_break.setValue(line_break)
        self.textedit_separator.setText(separator)
        self.textedit_front_str.setText(front_string)
        self.textedit_end_str.setText(end_string)

    def getSettings(self):
        self.settings_obj.setValue("line_break", self.spinbox_line_break.value())
        self.settings_obj.setValue("separator", self.textedit_separator.text())
        self.settings_obj.setValue("front_string", self.textedit_front_str.text())
        self.settings_obj.setValue("end_string", self.textedit_end_str.text())
        self.settings_obj.sync()
        return self.settings_obj

    