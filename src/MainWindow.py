import typing
import io

from PyQt5.QtCore import QSize, Qt, QSettings
from PyQt5.QtGui import QFont, QPixmap, QImage, QClipboard
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow, 
    QWidget, 
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QTextEdit,
    QFileDialog,
    QSlider,
    QMessageBox,
    QLabel)

from PIL import Image
from .Core import processImage, pretreatment, numpy2image
from .SettingsDialog import SettingWindow

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        # Initial settings
        self.setFixedSize(QSize(600, 500))
        self.setWindowTitle("HexPicGenerator")

        # Data
        self.image = None # The original image
        self.image_processed = None # The image to be processed, PIL Image

        # Settings
        self.settings_obj = None
        self.line_break = 16
        self.separator = ""
        self.front_string = ""
        self.end_string = ""

        self.vbox_global = QVBoxLayout()

        # The upper part: an image preview widget
        self.label_origin_img_caption = QLabel("图像预览：")
        self.label_origin_img_preview = QLabel("请打开图像")
        self.label_origin_img_preview.setFixedHeight(200)
        self.label_origin_img_preview.setAlignment(Qt.AlignCenter)

        # The lower part: output and buttons
        self.label_operations = QLabel("操作：")
        self.hbox_button = QHBoxLayout()
        self.button_addpic = QPushButton("打开图像")
        self.button_settings = QPushButton("更改设置")
        self.button_gen = QPushButton("生成结果")
        self.button_copy = QPushButton("拷贝至剪贴板")
        

        self.hbox_slider = QHBoxLayout()
        self.label_slider = QLabel("阈值")
        self.slider_thresh = QSlider(Qt.Orientation.Horizontal)
        self.slider_thresh.setValue(128)
        self.slider_thresh.setRange(0, 255)

        self.hbox_slider.addWidget(self.label_slider)
        self.hbox_slider.addWidget(self.slider_thresh)
        
        self.hbox_button.addWidget(self.button_addpic)
        self.hbox_button.addWidget(self.button_settings)
        self.hbox_button.addWidget(self.button_gen)
        self.hbox_button.addWidget(self.button_copy)

        self.label_text_output = QLabel("输出结果：")
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        self.text_output.setFont(QFont("Courier"))

        # Add the widgets to the layout
        self.vbox_global.addWidget(self.label_origin_img_caption)
        self.vbox_global.addWidget(self.label_origin_img_preview)
        self.vbox_global.addWidget(self.label_operations)
        self.vbox_global.addLayout(self.hbox_button)
        self.vbox_global.addLayout(self.hbox_slider)
        self.vbox_global.addWidget(self.label_text_output)
        self.vbox_global.addWidget(self.text_output)

        self.container = QWidget()
        self.container.setLayout(self.vbox_global)
        self.setCentralWidget(self.container)

        # Action bindings
        self.button_addpic.clicked.connect(self.onOpenImageClicked)
        self.button_settings.clicked.connect(self.onSettingsButtonClicked)
        self.button_gen.clicked.connect(self.onGenerateResultClicked)
        self.button_copy.clicked.connect(self.onCopyToClipboardClicked)
        self.slider_thresh.valueChanged.connect(self.sliderValueChanged)

    def Image_to_ImageQt(self, image : Image):
        # Need to rewrite the toqpixmap function. Imageqt does not work.
        # https://stackoverflow.com/questions/28086613/pillow-pil-to-qimage-conversion-python-exe-has-stopped-working
        bytes_img = io.BytesIO()
        image.save(bytes_img, format='PNG')

        qimg = QImage()
        qimg.loadFromData(bytes_img.getvalue())

        return QPixmap.fromImage(qimg)

    def refreshImagePreview(self):
        # Refresh the image preview label
        image_preview_qpixmap = self.Image_to_ImageQt(self.image_processed)
        self.label_origin_img_preview.setPixmap(image_preview_qpixmap.scaledToHeight(self.label_origin_img_preview.height()))

    def onOpenImageClicked(self):
        # Add image from local folder to the list
        file_info = QFileDialog.getOpenFileNames(self, "选择图片", "./", "图像文件 (*.jpg *.jpeg *.png)")
        file_names = file_info[0]
        for filename in file_names:
            if filename != '':
                self.image = Image.open(filename)
                self.image_processed = numpy2image(pretreatment(self.image, self.slider_thresh.value()))
                self.refreshImagePreview()

    def onSettingsButtonClicked(self):
        # Go to settings
        msg = SettingWindow(self, self.settings_obj)
        if msg.exec_():
            self.settings_obj = msg.getSettings()
            self.applySettings(self.settings_obj)


    def onGenerateResultClicked(self):
        # Generate the results
        if self.image:
            out_str = processImage(self.image, 
                                self.slider_thresh.value(), 
                                sep=self.separator, 
                                line_break_num=self.line_break,
                                front_str=self.front_string,
                                end_str=self.end_string)
            self.text_output.setText(out_str)
        else:
            QMessageBox.warning(self, "警告", "没有选择图片")
        

    def onCopyToClipboardClicked(self):
        # Copy the results onto the system clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_output.toPlainText())

    def sliderValueChanged(self):
        # Refresh the image preview when the value of the slider is changed
        if self.image:
            self.image_processed = numpy2image(pretreatment(self.image, self.slider_thresh.value()))
            self.refreshImagePreview()

    def applySettings(self, settings_obj : QSettings):
        # Receive a QSettings object and apply
        self.settings_obj = settings_obj
        self.line_break = int(settings_obj.value("line_break"))
        self.separator = settings_obj.value("separator")
        self.front_string = settings_obj.value("front_string")
        self.end_string = settings_obj.value("end_string")


        