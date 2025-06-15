from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QScrollArea
)
import time
from src.gui.components.sidebar import Sidebar
from src.gui.components.result_view import ResultsPanel

from src.controller.Controller import Controller
from src.database.db_config import *

class AnalyzePage(QWidget):
    def __init__(self, page_change):
        super().__init__()

        self.data = {}

        conn = connect()
        self.controller = Controller(conn)

        layout = QHBoxLayout(self)

        self.sidebar = Sidebar()
        self.sidebar.submit_clicked.connect(self.submit)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.results = ResultsPanel(page_change)
        self.results.setStyleSheet("border: none;")
        scroll_area.setWidget(self.results)
        scroll_area.setStyleSheet("border: none;")

        layout.addWidget(self.sidebar)
        layout.addWidget(scroll_area)

    def submit(self):
        start_time = time.time()
        (keyword, toggle, maxs) = self.sidebar.get_parameter()
        self.data = self.controller.searchQuery(keyword, toggle, maxs)
        end_time = time.time()
        elapsed_ms = (end_time - start_time) * 1000
        self.results.update_result(self.data, elapsed_ms)
