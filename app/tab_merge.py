from PyQt5.QtWidgets import *
import os
from utils import *


class MergeList(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.parent = parent
        self.elements_list = []  # [{"label": "PDF 1", "elements": QWidget()}, {...}, ...]
        self.add_row()
        self.add_row()

    def get_highest_row_id(self):
        highest_row_id = 0
        for row in self.elements_list:
            if row["row_id"] > highest_row_id:
                highest_row_id = row["row_id"]
        return highest_row_id

    def find_index_of_row_by_id(self, row_id):
        for row in range(len(self.elements_list)):
            if self.elements_list[row]["row_id"] == row_id:
                return row

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
        pixmap = getattr(QStyle, "SP_TitleBarShadeButton")
        icon = self.style().standardIcon(pixmap)
        button_up.setIcon(icon)
        widget_layout.addWidget(button_up)
        #
        button_down = QButton(f"button_down_{amount}", "", self)
        pixmap = getattr(QStyle, "SP_TitleBarUnshadeButton")
        icon = self.style().standardIcon(pixmap)
        button_down.setIcon(icon)
        widget_layout.addWidget(button_down)

        button_down = QButton(f"button_remove_{amount}", "", self)
        pixmap = getattr(QStyle, "SP_DialogCancelButton")
        icon = self.style().standardIcon(pixmap)
        button_down.setIcon(icon)
        widget_layout.addWidget(button_down)

        self.elements_list.append({
            "row_id": amount,
            "label": QLineEdit(f"PDF file {amount}"),
            "element": widget
        })
        #
        self.re_render()

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
            line_edit = self.parent.findChild(QLineEdit, f"line_edit_{row_id}")
            line_edit_content = line_edit.text()
            if line_edit_content:
                file_path, _ = QFileDialog.getOpenFileName(self, f"Select PDF {row_id}",
                                                           line_edit_content, "PDF (*.pdf)")
            else:
                user_dir = os.path.join(os.path.expanduser("~"), "Documents")
                file_path, _ = QFileDialog.getOpenFileName(self, f"Select PDF {row_id}", user_dir, "PDF (*.pdf)")
            if file_path:
                line_edit.setText(file_path)

    def re_render(self):
        main_list_widget = QWidget()
        main_form = QFormLayout()

        for i in range(len(self.elements_list)):
            main_form.addRow(self.elements_list[i]["label"], self.elements_list[i]["element"])

        main_list_widget.setLayout(main_form)
        self.parent.scroll.setWidget(main_list_widget)
