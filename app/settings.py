from PyQt5 import uic
from PyQt5.QtWidgets import *
from utils import *


def change_window_style(app, value):
    if value == "windowsvista":
        app.setStyle('windowsvista')
    elif value == "Windows":
        app.setStyle('Windows')
    elif value == "Fusion":
        app.setStyle('Fusion')


class SettingsWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        uic.loadUi('settings_window.ui', self)  # Load the .ui file
        window_style = self.findChild(QComboBox, "comboBox_window_style")

        settings = read_settings()
        if settings is not None:
            index = window_style.findText(settings[WINDOW_STYLE_KEY])
            if index >= 0:
                window_style.setCurrentIndex(index)
        window_style.currentTextChanged.connect(self.on_window_style_changed)
        button_close = self.findChild(QPushButton, "pushButton_close")
        button_close.clicked.connect(self.close)

    def on_window_style_changed(self, value):
        write_settings({
            WINDOW_STYLE_KEY: value
        })
        change_window_style(self.app, value)
