import sys, os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import qdarktheme

from pypdf import PdfMerger
from pathlib import Path

output_path = os.path.join(os.path.expanduser("~"), "Documents", "result.pdf")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # Call the inherited classes __init__ method
        uic.loadUi('main_window.ui', self)  # Load the .ui file
        self.setWindowTitle("PDF Merge")

        self.layout = self.findChild(QVBoxLayout, "verticalLayout_main")
        self.scroll = QScrollArea()
        self.button_add_documents = self.findChild(QPushButton, "pushButton_add")
        self.button_add_documents.clicked.connect(self.add_row)
        line_edit_output_path = self.findChild(QLineEdit, "lineEdit_output")
        line_edit_output_path.setText(output_path)
        button_output_path = self.findChild(QPushButton, "pushButton_browse_output_path")
        button_output_path.clicked.connect(self.browse_output_path)
        button_merge = self.findChild(QPushButton, "pushButton_merge")
        button_merge.clicked.connect(self.merge_pdfs)

        self.elements_list = []  # [{"label": "PDF 1", "elements": QWidget()}, {...}, ...]
        self.add_row()
        self.add_row()

        self.scroll.setWidgetResizable(True)
        self.layout.addWidget(self.scroll)


    def add_row(self):
        amount = self.get_highest_row_id() + 1

        widget = QWidget()
        widget_layout = QHBoxLayout()
        widget_layout.setContentsMargins(0, 0, 0, 10)

        widget.setLayout(widget_layout)
        line_edit = QLineEdit()
        line_edit.setObjectName(f"line_edit_{amount}")
        widget_layout.addWidget(line_edit)

        button_browse = QButton(f"button_browse_{amount}", "...", self)
        button_browse.setMaximumWidth(30)
        widget_layout.addWidget(button_browse)

        button_up = QButton(f"button_up_{amount}", "", self)
        pixmapi = getattr(QStyle, "SP_TitleBarShadeButton")
        icon = self.style().standardIcon(pixmapi)
        button_up.setIcon(icon)
        widget_layout.addWidget(button_up)

        button_down = QButton(f"button_down_{amount}", "", self)
        pixmapi = getattr(QStyle, "SP_TitleBarUnshadeButton")
        icon = self.style().standardIcon(pixmapi)
        button_down.setIcon(icon)
        widget_layout.addWidget(button_down)

        button_down = QButton(f"button_remove_{amount}", "", self)
        pixmapi = getattr(QStyle, "SP_DialogCancelButton")
        icon = self.style().standardIcon(pixmapi)
        button_down.setIcon(icon)
        widget_layout.addWidget(button_down)

        self.elements_list.append({
            "row_id": amount,
            "label": QLabel(f"PDF file {amount}"),
            "element": widget
        })

        self.re_render()


    def re_render(self):
        self.main_list_widget = QWidget()
        self.main_form = QFormLayout()

        for i in range(len(self.elements_list)):
            self.main_form.addRow(self.elements_list[i]["label"], self.elements_list[i]["element"])

        self.main_list_widget.setLayout(self.main_form)
        self.scroll.setWidget(self.main_list_widget)


    def find_index_of_row_by_id(self, row_id):
        for row in range(len(self.elements_list)):
            if self.elements_list[row]["row_id"] == row_id:
                return row


    def get_highest_row_id(self):
        highest_row_id = 0
        for row in self.elements_list:
            if row["row_id"] > highest_row_id:
                highest_row_id = row["row_id"]
        return highest_row_id


    def perform_button_action(self, button_id):
        actions = button_id.split("_")
        row_id = int(actions[2])
        index = self.find_index_of_row_by_id(row_id)
        action = actions[1]

        row = self.elements_list[index]

        if action == "up":
            self.elements_list.remove(row)
            new_index = index - 1
            if new_index < 0:
                new_index = 0
            self.elements_list.insert(new_index, row)
            self.re_render()
        elif action == "down":
            self.elements_list.remove(row)
            new_index = index + 1
            self.elements_list.insert(new_index, row)
            self.re_render()
        elif action == "remove":
            self.elements_list.remove(row)
            self.re_render()
        elif action == "browse":

            line_edit = self.findChild(QLineEdit, f"line_edit_{row_id}")
            line_edit_content = line_edit.text()
            if line_edit_content:
                file_path, _ = QFileDialog.getOpenFileName(self, f"Select PDF {row_id}", line_edit_content, "PDF (*.pdf)")
            else:
                user_dir = os.path.join(os.path.expanduser("~"), "Documents")
                file_path, _ = QFileDialog.getOpenFileName(self, f"Select PDF {row_id}", user_dir, "PDF (*.pdf)")
            if file_path:
                line_edit.setText(file_path)


    def browse_output_path(self):
        line_edit = self.findChild(QLineEdit, "lineEdit_output")
        line_edit_content = line_edit.text()
        if line_edit_content:
            file_path, _ = QFileDialog.getSaveFileName(self, "Select output PDF location", line_edit_content, "PDF (*.pdf)")
        else:
            user_dir = os.path.join(os.path.expanduser("~"), "Documents")
            file_path, _ = QFileDialog.getSaveFileName(self, "Select output PDF location", user_dir, "PDF (*.pdf)")
        if file_path:
            line_edit.setText(file_path)


    def merge_pdfs(self):
        pdf_list = []

        for row in self.elements_list:
            row_id = row["row_id"]
            line_edit = self.findChild(QLineEdit, f"line_edit_{row_id}")
            line_edit_content = line_edit.text()
            pdf_list.append(line_edit_content)

        line_edit_output_path = self.findChild(QLineEdit, "lineEdit_output")
        output_path = line_edit_output_path.text()

        if len(pdf_list) <= 1:
            show_dialog("Error", "Please specify at least two documents to merge.", QMessageBox.Critical)
            return

        merger = PdfMerger()

        try:
            for pdf in pdf_list:
                merger.append(pdf)

            new_file = Path(output_path)
            if new_file.is_file():
                override_existing_file = show_dialog("Override file",
                                                     f"File {output_path} already exists. Do you want to override it?",
                                                     QMessageBox.Question, show_two_buttons=True)
                if override_existing_file:
                    merger.write(output_path)
                    show_dialog("Success", f"New PDF created: {output_path}", QMessageBox.Information)
            else:
                merger.write(output_path)
                show_dialog("Success", f"New PDF created: {output_path}", QMessageBox.Information)
        except Exception as e:
            show_dialog("Error", str(e), QMessageBox.Critical)
        finally:
            merger.close()


class QButton(QPushButton):
    def __init__(self, button_id, label, parent=None):
        QPushButton.__init__(self, label)
        self.button_id = button_id
        self.parent: MainWindow = parent
        self.clicked.connect(self.call_action)

    def call_action(self):
        self.parent.perform_button_action(self.button_id)


def show_dialog(title, description, type, show_two_buttons=False):
    msg_box = QMessageBox()
    msg_box.setIcon(type)
    msg_box.setWindowTitle(title)
    msg_box.setText(description)
    if show_two_buttons:
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    else:
        msg_box.setStandardButtons(QMessageBox.Ok)
    return_value = msg_box.exec()
    if return_value == QMessageBox.Ok:
        return True
    return False


if __name__ == '__main__':
    print(QtWidgets.QStyleFactory.keys())
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("dark")
    # app.setStyle('Fusion')
    wnd = MainWindow()
    wnd.show()
    sys.exit(app.exec_())