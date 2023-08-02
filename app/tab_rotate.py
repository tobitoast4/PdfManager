import sys, os
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import *
import qdarktheme

from pypdf import PdfMerger
from pathlib import Path


output_path = os.path.join(os.path.expanduser("~"), "Documents", "result.pdf")

class TabRotate():
    def __init__(self, main_window):
        self.main_window = main_window

    def initialize_tab(self):
        button_output_path = self.main_window.findChild(QPushButton, "rotate_pushButton_browse_output_path")
        button_output_path.clicked.connect(self.browse_rotate_output_path)
        line_edit_output_path = self.main_window.findChild(QLineEdit, "rotate_lineEdit_output")
        line_edit_output_path.setText(output_path)

        rotate_comboBox_degrees = self.main_window.findChild(QComboBox, "rotate_comboBox_degrees")
        index = rotate_comboBox_degrees.findText("180°", QtCore.Qt.MatchFixedString)
        if index >= 0:
            rotate_comboBox_degrees.setCurrentIndex(index)
        print(rotate_comboBox_degrees.currentText())


    def browse_rotate_output_path(self):
        print("asdfasfsf")
        # line_edit = self.main_window.findChild(QLineEdit, "rotate_lineEdit_output")
        # line_edit_content = line_edit.text()
        # if line_edit_content:
        #     file_path, _ = QFileDialog.getSaveFileName(self.main_window, "Select output PDF location",
        #                                                line_edit_content, "PDF (*.pdf)")
        # else:
        #     user_dir = os.path.join(os.path.expanduser("~"), "Documents")
        #     file_path, _ = QFileDialog.getSaveFileName(self.main_window, "Select output PDF location", user_dir,
        #                                                "PDF (*.pdf)")
        # if file_path:
        #     line_edit.setText(file_path)