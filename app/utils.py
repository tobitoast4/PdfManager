from PyQt5.QtWidgets import QMessageBox, QPushButton
from pypdf import PdfMerger, PdfWriter, PdfReader
from pathlib import Path
import json

WINDOW_STYLE_KEY = "window_style"


def write_settings(json_data):
    json_object = json.dumps(json_data, indent=4)
    with open("res/settings.json", "w") as outfile:
        outfile.write(json_object)


def read_settings():
    try:
        with open('res/settings.json', 'r') as openfile:
            return json.load(openfile)
    except FileNotFoundError:
        return None


class QButton(QPushButton):
    def __init__(self, button_id, label, parent=None):
        QPushButton.__init__(self, label)
        self.button_id = button_id
        self.parent = parent
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


def merge_pdfs(pdf_list, output_path):
    if output_path == "":
        show_dialog("Error", "Output path should not be empty.", QMessageBox.Critical)
        return
    if len(pdf_list) <= 1:
        show_dialog("Error", "Please specify at least two documents to merge.", QMessageBox.Critical)
        return

    merger = PdfMerger()

    try:
        for pdf in pdf_list:
            if pdf == "":
                show_dialog("Error", "No input path should be empty.", QMessageBox.Critical)
                return
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


def split_pdf(input_path, output_path, selected_pages):
    if input_path == "":
        show_dialog("Error", "Input path should not be empty.", QMessageBox.Critical)
        return
    if output_path == "":
        show_dialog("Error", "Output path should not be empty.", QMessageBox.Critical)
        return
    writer = PdfWriter()
    try:
        reader = PdfReader(input_path)
        selected_pages_list = get_page_list_from_selected_pages(selected_pages)
        for page in range(len(reader.pages)):
            if page in selected_pages_list:
                writer.add_page(reader.pages[page])

        save_output_file(writer, output_path)
    except Exception as e:
        show_dialog("Error", str(e), QMessageBox.Critical)


def rotate_pdf(input_path, output_path, rotation_degrees, selected_pages):
    if input_path == "":
        show_dialog("Error", "Input path should not be empty.", QMessageBox.Critical)
        return
    if output_path == "":
        show_dialog("Error", "Output path should not be empty.", QMessageBox.Critical)
        return
    writer = PdfWriter()
    try:
        reader = PdfReader(input_path)
        rotation_degrees = int(str(rotation_degrees)[:-1])

        selected_pages_list = get_page_list_from_selected_pages(selected_pages)

        for page in range(len(reader.pages)):
            if selected_pages is None or page in selected_pages_list:   # if selected_pages is None -> all pages should
                writer.add_page(reader.pages[page])                     # be rotated; or if page in in the list of the
                writer.pages[page].rotate(rotation_degrees)             # ones to be rotated
        save_output_file(writer, output_path)
    except Exception as e:
        show_dialog("Error", str(e), QMessageBox.Critical)
    finally:
        writer.close()


def get_page_list_from_selected_pages(selected_pages: str):
    try:
        selected_pages_list = []
        if selected_pages is None:
            return selected_pages_list
        selected_pages = selected_pages.replace(" ", "")  # remove whitespaces
        if len(selected_pages) <= 0:
            raise ValueError("Please enter some pages.")
        chars = set('0123456789-,')
        if any((c not in chars) for c in selected_pages):  # check for invalid characters
            raise ValueError("Invalid character found. Valid characters: 0 1 2 3 4 5 6 7 8 9 - ,")
        page_ranges = selected_pages.split(",")
        for page_range in page_ranges:
            if "-" in page_range:  # current page range is a range
                page_range_split = page_range.split("-")
                selected_pages_list += [*range(int(page_range_split[0]), int(page_range_split[1]))]
                selected_pages_list.append(int(page_range_split[1]))
            else:                  # current page range is a single page number
                selected_pages_list.append(int(page_range))
        selected_pages_list = [page_nr-1 for page_nr in selected_pages_list]
        return selected_pages_list
    except Exception as e:
        raise ValueError(f"The input for the selected pages is not valid.\n\n(Error: {e})")


def save_output_file(pdf_writer: PdfWriter, output_path):
    new_file = Path(output_path)
    if new_file.is_file():
        override_existing_file = show_dialog("Override file",
                                             f"File {output_path} already exists. Do you want to override it?",
                                             QMessageBox.Question, show_two_buttons=True)
        if override_existing_file:
            with open(output_path, "wb") as fp:
                pdf_writer.write(fp)
            show_dialog("Success", f"New PDF created: {output_path}", QMessageBox.Information)
    else:
        with open(output_path, "wb") as fp:
            pdf_writer.write(fp)
        show_dialog("Success", f"New PDF created: {output_path}", QMessageBox.Information)


def remove_quotes_from_path(path: str):
    if path is None or path == "":
        return ""
    if (path[0] == '"' and path[-1] == '"') or (path[0] == "'" and path[-1] == "'"):
        return path[1:-1]
    return path
