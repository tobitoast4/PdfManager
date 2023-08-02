import sys, os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import qdarktheme

from tab_merge import TabMerge
from tab_rotate import TabRotate


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # Call the inherited classes __init__ method
        uic.loadUi('main_window.ui', self)  # Load the .ui file
        self.setWindowTitle("PDF Merge")

        tab_merge = TabMerge(self)
        tab_merge.initialize_tab()
        tab_rotate = TabRotate(self)
        tab_rotate.initialize_tab()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("light")
    # print(QtWidgets.QStyleFactory.keys())
    # app.setStyle('Fusion')
    wnd = MainWindow()
    wnd.show()
    sys.exit(app.exec_())