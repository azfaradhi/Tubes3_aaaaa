import sys, os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QScrollArea
)
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtCore import Qt
from gui.components.sidebar import Sidebar
from gui.components.result_view import ResultsPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CV Analyzer ATS")
        self.resize(1000, 700)

        container = QWidget()
        container.setStyleSheet("background-color: #FFF8DC;")

        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #F4F4F4;")

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(80, 80, 80, 80)
        container_layout.addWidget(central_widget)

        content_layout = QHBoxLayout()

        sidebar = Sidebar()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        results = ResultsPanel()
        results.setStyleSheet("border: none;")
        scroll_area.setWidget(results)
        scroll_area.setStyleSheet("border: none;")

        content_layout.addWidget(sidebar)
        content_layout.addWidget(scroll_area)

        main_layout.addLayout(content_layout)

        container.setLayout(main_layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # ------------- font -------------
    font_id = QFontDatabase.addApplicationFont(
        os.path.join(os.path.dirname(__file__), "assets", "Poppins-Regular.ttf")
    )
    family = QFontDatabase.applicationFontFamilies(font_id)[0]
    app.setFont(QFont(family, 10))


    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
