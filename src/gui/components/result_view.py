from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea
from PyQt5.QtCore import Qt
from gui.components.result_card import Card

class ResultsPanel(QWidget):
    def __init__(self, page_change):
        super().__init__()
        outer_layout = QVBoxLayout(self)

        title = QLabel("Result")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            "color: #2c3e50;" \
            "font-size: 16pt; " \
            "font-weight: bold;" \
            "text-align: center;"
        )
        self.setStyleSheet("background: transparent;")
        outer_layout.addWidget(title)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background: transparent;")

        content_widget = QWidget()
        card_grid = QGridLayout(content_widget)
        content_widget.setStyleSheet("background: transparent;")
        card_grid.setSpacing(20)
        card_grid.setContentsMargins(10, 10, 10, 10)

        # Add more than 4 cards to demonstrate scrolling
        for i in range(10):
            card = Card(page_change, f"Card {i+1}")
            row = i // 2
            col = i % 2
            card_grid.addWidget(card, row, col)

        scroll_area.setWidget(content_widget)
        outer_layout.addWidget(scroll_area)