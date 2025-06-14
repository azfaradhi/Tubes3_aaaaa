# main.py
import sys, os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QStackedWidget
)
from PyQt5.QtGui import QFontDatabase, QFont
from gui.pages.analyze_page import AnalyzePage
from gui.pages.landing_page import LandingPage
from gui.pages.detail_page import DetailPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CV Analyzer ATS")
        self.resize(1000, 700)

        outer_container = QWidget()
        outer_container.setStyleSheet("background-color: #FFF8DC;")
        outer_layout = QVBoxLayout(outer_container)
        outer_layout.setContentsMargins(80, 80, 80, 80)

        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #F4F4F4; border-radius: 15px;")
        central_layout = QVBoxLayout(central_widget)

        self.stack = QStackedWidget()
        self.page_landing = LandingPage(self.change_page)
        self.page_analyze = AnalyzePage(self.change_page)
        self.page_detail = DetailPage(self.change_page)

        self.stack.addWidget(self.page_landing)  # index 0
        self.stack.addWidget(self.page_analyze)  # index 1
        self.stack.addWidget(self.page_detail)   # index 2

        central_layout.addWidget(self.stack)
        outer_layout.addWidget(central_widget)

        self.setCentralWidget(outer_container)

    def change_page(self, index, path=None):
        if index == 2 and path is not None:
            self.page_detail.load_path(path)
        self.stack.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    font_id = QFontDatabase.addApplicationFont(
        os.path.join(os.path.dirname(__file__), "assets", "Poppins-Regular.ttf")
    )
    family = QFontDatabase.applicationFontFamilies(font_id)[0]
    app.setFont(QFont(family, 10))

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
