def add_row(self, self.main_window):
    amount = self.main_window.get_highest_row_id() + 1

    widget = QWidget()
    widget_layout = QHBoxLayout()
    widget_layout.setContentsMargins(0, 0, 0, 10)

    widget.setLayout(widget_layout)
    line_edit = QLineEdit()
    line_edit.setObjectName(f"line_edit_{amount}")
    widget_layout.addWidget(line_edit)

    button_browse = QButton(f"button_browse_{amount}", "...", self.main_window)
    button_browse.setMaximumWidth(30)
    widget_layout.addWidget(button_browse)

    button_up = QButton(f"button_up_{amount}", "", self.main_window)
    pixmapi = getattr(QStyle, "SP_TitleBarShadeButton")
    icon = self.main_window.style().standardIcon(pixmapi)
    button_up.setIcon(icon)
    widget_layout.addWidget(button_up)

    button_down = QButton(f"button_down_{amount}", "", self.main_window)
    pixmapi = getattr(QStyle, "SP_TitleBarUnshadeButton")
    icon = self.main_window.style().standardIcon(pixmapi)
    button_down.setIcon(icon)
    widget_layout.addWidget(button_down)

    button_down = QButton(f"button_remove_{amount}", "", self.main_window)
    pixmapi = getattr(QStyle, "SP_DialogCancelButton")
    icon = self.main_window.style().standardIcon(pixmapi)
    button_down.setIcon(icon)
    widget_layout.addWidget(button_down)

    self.main_window.elements_list.append({
        "row_id": amount,
        "label": QLineEdit(f"PDF file {amount}"),
        "element": widget
    })

    self.main_window.re_render()


def re_render(self, self.main_window):
    self.main_window.main_list_widget = QWidget()
    self.main_window.main_form = QFormLayout()

    for i in range(len(self.main_window.elements_list)):
        self.main_window.main_form.addRow(self.main_window.elements_list[i]["label"], self.main_window.elements_list[i]["element"])

    self.main_window.main_list_widget.setLayout(self.main_window.main_form)
    self.main_window.scroll.setWidget(self.main_window.main_list_widget)


def find_index_of_row_by_id(self, self.main_window, row_id):
    for row in range(len(self.main_window.elements_list)):
        if self.main_window.elements_list[row]["row_id"] == row_id:
            return row


def get_highest_row_id(self, self.main_window):
    highest_row_id = 0
    for row in self.main_window.elements_list:
        if row["row_id"] > highest_row_id:
            highest_row_id = row["row_id"]
    return highest_row_id


def perform_button_action(self, self.main_window, button_id):
    actions = button_id.split("_")
    row_id = int(actions[2])
    index = self.main_window.find_index_of_row_by_id(row_id)
    action = actions[1]

    row = self.main_window.elements_list[index]

    if action == "up":
        self.main_window.elements_list.remove(row)
        new_index = index - 1
        if new_index < 0:
            new_index = 0
        self.main_window.elements_list.insert(new_index, row)
        self.main_window.re_render()
    elif action == "down":
        self.main_window.elements_list.remove(row)
        new_index = index + 1
        self.main_window.elements_list.insert(new_index, row)
        self.main_window.re_render()
    elif action == "remove":
        self.main_window.elements_list.remove(row)
        self.main_window.re_render()
    elif action == "browse":
        line_edit = self.main_window.findChild(QLineEdit, f"line_edit_{row_id}")
        line_edit_content = line_edit.text()
        if line_edit_content:
            file_path, _ = QFileDialog.getOpenFileName(self.main_window, f"Select PDF {row_id}", line_edit_content, "PDF (*.pdf)")
        else:
            user_dir = os.path.join(os.path.expanduser("~"), "Documents")
            file_path, _ = QFileDialog.getOpenFileName(self.main_window, f"Select PDF {row_id}", user_dir, "PDF (*.pdf)")
        if file_path:
            line_edit.setText(file_path)


def browse_output_path(self, self.main_window):
    line_edit = self.main_window.findChild(QLineEdit, "merge_lineEdit_output")
    line_edit_content = line_edit.text()
    if line_edit_content:
        file_path, _ = QFileDialog.getSaveFileName(self.main_window, "Select output PDF location", line_edit_content, "PDF (*.pdf)")
    else:
        user_dir = os.path.join(os.path.expanduser("~"), "Documents")
        file_path, _ = QFileDialog.getSaveFileName(self.main_window, "Select output PDF location", user_dir, "PDF (*.pdf)")
    if file_path:
        line_edit.setText(file_path)


def merge_pdfs(self, self.main_window):
    pdf_list = []

    for row in self.main_window.elements_list:
        row_id = row["row_id"]
        line_edit = self.main_window.findChild(QLineEdit, f"line_edit_{row_id}")
        line_edit_content = line_edit.text()
        pdf_list.append(line_edit_content)

    line_edit_output_path = self.main_window.findChild(QLineEdit, "merge_lineEdit_output")
    output_path = line_edit_output_path.text()

    if len(pdf_list) <= 1:
        misc.show_dialog("Error", "Please specify at least two documents to merge.", QMessageBox.Critical)
        return

    merger = PdfMerger()

    try:
        for pdf in pdf_list:
            merger.append(pdf)

        new_file = Path(output_path)
        if new_file.is_file():
            override_existing_file = misc.show_dialog("Override file",
                                                      f"File {output_path} already exists. Do you want to override it?",
                                                      QMessageBox.Question, show_two_buttons=True)
            if override_existing_file:
                merger.write(output_path)
                misc.show_dialog("Success", f"New PDF created: {output_path}", QMessageBox.Information)
        else:
            merger.write(output_path)
            misc.show_dialog("Success", f"New PDF created: {output_path}", QMessageBox.Information)
    except Exception as e:
        misc.show_dialog("Error", str(e), QMessageBox.Critical)
    finally:
        merger.close()