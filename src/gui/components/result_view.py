from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea
from PyQt5.QtCore import Qt
from gui.components.result_card import Card

class ResultsPanel(QWidget):
    def __init__(self, page_change):
        super().__init__()
        outer_layout = QVBoxLayout(self)
        self.page_change = page_change

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
        self.card_grid = QGridLayout(content_widget)
        content_widget.setStyleSheet("background: transparent;")
        self.card_grid.setSpacing(20)
        self.card_grid.setContentsMargins(10, 10, 10, 10)

        scroll_area.setWidget(content_widget)
        outer_layout.addWidget(scroll_area)

    def update_result(self, data):
        print(data)
        # Delete data sebelum
        while self.card_grid.count():
            child = self.card_grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        for i, (key, value) in enumerate(data.items()):
            card = Card(
                self.page_change, 
                value['name'],
                value['cv_path'],
                value['keywords_count'],
                value['count']
            )
            row = i // 2
            col = i % 2
            self.card_grid.addWidget(card, row, col)
        return