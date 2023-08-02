import sys
import os
import glob

from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import (QMainWindow, QApplication, QMenu, QVBoxLayout,
                             QWidget, QAction, QFileDialog)
from PyQt5.QtGui import (QIcon, QKeySequence)
import qpageview


class MainWindow(QMainWindow):
    """Main Window."""

    def __init__(self, *args, **kwargs):
        """Initializer."""

        super(MainWindow, self).__init__(*args, **kwargs)

        self.window_title = 'Document Viewer'
        self.setWindowTitle(self.window_title)
        self.resize(600, 450)

        widget = QWidget()
        self.setCentralWidget(widget)

        self.layout = QVBoxLayout()
        widget.setLayout(self.layout)

        self._createImageViewer()
        self._createMenu()

    def _createImageViewer(self):

        self.viewer = qpageview.View()
        self.viewer.loadPdf(r"C:/Users/tobi-/Downloads/Profile (1).pdf")
        self.layout.addWidget(self.viewer)
        self.viewer.show()
        self.viewer.loadPdf(r"x.pdf")
        return

    def _createMenu(self):
        self.file_menu = self.menuBar().addMenu("&File")

        # File submenu
        self.openFileAction = QAction(QIcon.fromTheme('document-open'),
                                      '&Open', self, shortcut=QKeySequence.Open,
                                      triggered=self.openFile)
        self.file_menu.addAction(self.openFileAction)

    def openFile(self):
        fileName, _ = QFileDialog().getOpenFileName(self,
                                                    "Open Documents", QDir.currentPath(),
                                                    "PDF (*.pdf)"
                                                    + ";;" + "PNG (*.png)"
                                                    + ";;" + "JPEG (*.jpg *.jpeg)"
                                                    + ";;" + "SVG (*.svg)"
                                                    )
        if fileName:
            ext = os.path.splitext(fileName)[1]
            if ext == '.pdf':
                self.viewer.loadPdf(fileName)
            elif ext == '.jpg' or ext == '.jpeg' or ext == '.png':
                self.viewer.loadImages(glob.glob(fileName))
            elif ext == '.svg':
                self.viewer.loadSvgs(glob.glob(fileName))
            self.viewer.setViewMode(qpageview.FitWidth)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())