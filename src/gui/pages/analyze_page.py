from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QScrollArea
)

from gui.components.sidebar import Sidebar
from gui.components.result_view import ResultsPanel

class AnalyzePage(QWidget):
    def __init__(self, page_change):
        super().__init__()
        layout = QHBoxLayout(self)

        sidebar = Sidebar()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        results = ResultsPanel(page_change)
        results.setStyleSheet("border: none;")
        scroll_area.setWidget(results)
        scroll_area.setStyleSheet("border: none;")

        layout.addWidget(sidebar)
        layout.addWidget(scroll_area)
