import sys
from PyQt5 import uic, QtCore

from tab_merge import *
from settings import SettingsWindow, change_window_style

output_path = os.path.join(os.path.expanduser("~"), "Documents", "result.pdf")
app = QApplication(sys.argv)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)  # Load the .ui file

        self.layout = self.findChild(QVBoxLayout, "verticalLayout_main")
        self.scroll = QScrollArea()
        self.merge_list_widget = MergeList(self)

        button_settings = self.findChild(QPushButton, "pushButton_settings")
        pixmap = getattr(QStyle, "SP_MessageBoxQuestion")
        icon = self.style().standardIcon(pixmap)
        button_settings.setIcon(icon)
        button_settings.clicked.connect(self.show_settings)

        # merge tab
        self.button_add_documents = self.findChild(QPushButton, "pushButton_add")
        self.button_add_documents.clicked.connect(self.merge_list_widget.add_row)
        line_edit_output_path = self.findChild(QLineEdit, "merge_lineEdit_output")
        line_edit_output_path.setText(output_path)
        merge_button_output_path = self.findChild(QPushButton, "merge_pushButton_browse_output_path")
        merge_button_output_path.clicked.connect(lambda: self.browse_path_output("merge"))
        button_merge = self.findChild(QPushButton, "pushButton_merge")
        button_merge.clicked.connect(self.merge_pdfs)
        self.scroll.setWidgetResizable(True)
        self.layout.addWidget(self.scroll)

        # split tab
        line_edit_output_path = self.findChild(QLineEdit, "split_lineEdit_output")
        line_edit_output_path.setText(output_path)
        split_button_input_path = self.findChild(QPushButton, "split_pushButton_browse_input_path")
        split_button_input_path.clicked.connect(lambda: self.browse_path_input("split"))
        split_button_output_path = self.findChild(QPushButton, "split_pushButton_browse_output_path")
        split_button_output_path.clicked.connect(lambda: self.browse_path_output("split"))
        button_split = self.findChild(QPushButton, "pushButton_split")
        button_split.clicked.connect(self.split_pdf)

        # rotate tab
        rotate_button_input_path = self.findChild(QPushButton, "rotate_pushButton_browse_input_path")
        rotate_button_input_path.clicked.connect(lambda: self.browse_path_input("rotate"))
        self.line_edit_output_path_rotate = self.findChild(QLineEdit, "rotate_lineEdit_output")
        self.line_edit_output_path_rotate.setText(output_path)
        rotate_button_output_path = self.findChild(QPushButton, "rotate_pushButton_browse_output_path")
        rotate_button_output_path.clicked.connect(lambda: self.browse_path_output("rotate"))
        self.widget_select_pages = self.findChild(QWidget, "rotate_widget_select_pages")
        self.widget_select_pages.setVisible(False)
        self.checkBox_select_pages = self.findChild(QCheckBox, "rotate_checkBox_select_pages")
        self.checkBox_select_pages.stateChanged.connect(self.rotate_all_pages_changed)
        self.rotate_comboBox_degrees = self.findChild(QComboBox, "rotate_comboBox_degrees")
        index = self.rotate_comboBox_degrees.findText("180°", QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.rotate_comboBox_degrees.setCurrentIndex(index)
        button_rotate = self.findChild(QPushButton, "pushButton_rotate")
        button_rotate.clicked.connect(self.rotate_pdf)

    def browse_path_output(self, button_id_name):
        """Opens dialog to browse the output file.

        !!! The output QLineEdit is named: merge_lineEdit_output, split_lineEdit_output, rotate_lineEdit_output, ...
            -> Therefore this method can be reused.
        """
        line_edit = self.findChild(QLineEdit, f"{button_id_name}_lineEdit_output")
        line_edit_content = line_edit.text()
        if line_edit_content:
            file_path, _ = QFileDialog.getSaveFileName(self, "Select output PDF location",
                                                       line_edit_content, "PDF (*.pdf)")
        else:
            user_dir = os.path.join(os.path.expanduser("~"), "Documents")
            file_path, _ = QFileDialog.getSaveFileName(self, "Select output PDF location", user_dir,
                                                       "PDF (*.pdf)")
        if file_path:
            line_edit.setText(file_path)

    def browse_path_input(self, button_id_name):
        line_edit = self.findChild(QLineEdit, f"{button_id_name}_lineEdit_input")
        line_edit_content = line_edit.text()
        if line_edit_content:
            file_path, _ = QFileDialog.getOpenFileName(self, f"Select PDF", line_edit_content, "PDF (*.pdf)")
        else:
            user_dir = os.path.join(os.path.expanduser("~"), "Documents")
            file_path, _ = QFileDialog.getOpenFileName(self, f"Select PDF", user_dir, "PDF (*.pdf)")
        if file_path:
            line_edit.setText(file_path)

    def merge_pdfs(self):
        pdf_list = []

        for row in self.merge_list_widget.elements_list:
            row_id = row["row_id"]
            line_edit = self.findChild(QLineEdit, f"line_edit_{row_id}")
            line_edit_content = remove_quotes_from_path(line_edit.text())
            pdf_list.append(line_edit_content)

        line_edit_output_path = self.findChild(QLineEdit, "merge_lineEdit_output")
        output_path = remove_quotes_from_path(line_edit_output_path.text())
        merge_pdfs(pdf_list, output_path)

    def rotate_all_pages_changed(self):
        if self.checkBox_select_pages.isChecked():
            self.widget_select_pages.setVisible(False)
        else:
            self.widget_select_pages.setVisible(True)

    def split_pdf(self):
        line_edit_input_path = self.findChild(QLineEdit, "split_lineEdit_input")
        line_edit_output_path = self.findChild(QLineEdit, "split_lineEdit_output")
        line_edit_selected_pages = self.findChild(QLineEdit, "split_lineEdit_selected_pages")
        split_input_path = remove_quotes_from_path(line_edit_input_path.text())
        split_output_path = remove_quotes_from_path(line_edit_output_path.text())
        selected_pages = line_edit_selected_pages.text()
        split_pdf(split_input_path, split_output_path, selected_pages)

    def rotate_pdf(self):
        line_edit_input_path = self.findChild(QLineEdit, "rotate_lineEdit_input")
        rotate_input_path = remove_quotes_from_path(line_edit_input_path.text())
        rotate_output_path = remove_quotes_from_path(self.line_edit_output_path_rotate.text())
        rotation_degrees = self.rotate_comboBox_degrees.currentText()
        selected_pages = None
        if not self.checkBox_select_pages.isChecked():
            lineEdit_selected_pages = self.findChild(QLineEdit, "rotate_lineEdit_selected_pages")
            selected_pages = lineEdit_selected_pages.text()
        rotate_pdf(rotate_input_path, rotate_output_path, rotation_degrees, selected_pages)

    def show_settings(self):
            self.settings_wnd = SettingsWindow(app)
            self.settings_wnd.show()


if __name__ == '__main__':
    settings = read_settings()
    if settings is not None:
        change_window_style(app, settings[WINDOW_STYLE_KEY])
    wnd = MainWindow()
    wnd.show()
    sys.exit(app.exec_())