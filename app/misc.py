from PyQt5.QtWidgets import QMessageBox


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