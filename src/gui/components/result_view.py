from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea
from PyQt5.QtCore import Qt
from src.gui.components.result_card import Card

class ResultsPanel(QWidget):
    def __init__(self, page_change):
        super().__init__()
        outer_layout = QVBoxLayout(self)
        self.page_change = page_change

        title = QLabel("Result")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            color: #2c3e50;
            font-size: 20pt;
            font-weight: bold;
            text-align: center;
            padding: 10px;
        """)
        self.setStyleSheet("background-color: #FFFACD;")
        self.result_time_label = QLabel("")
        self.result_total_label = QLabel("")
        self.result_time_label.setStyleSheet("font-size: 12px; color: #555; margin-top: 10px;")
        self.result_total_label.setStyleSheet("font-size: 12px; color: #555; margin-top: 10px;")
        result_layout = QVBoxLayout()
        result_layout.addWidget(title)
        result_layout.addWidget(self.result_time_label)
        result_layout.addWidget(self.result_total_label)


        outer_layout.addLayout(result_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background: transparent; border: none;")

        content_widget = QWidget()
        self.card_grid = QGridLayout(content_widget)
        content_widget.setStyleSheet("background: transparent;")
        self.card_grid.setSpacing(20)
        self.card_grid.setContentsMargins(10, 10, 10, 10)

        scroll_area.setWidget(content_widget)
        outer_layout.addWidget(scroll_area)

    def update_result(self, data, time):
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
                value['count'],
                key
            )
            row = i // 2
            col = i % 2
            self.card_grid.addWidget(card, row, col)

        self.result_time_label.setText(f"Search time: {time:.2f} ms")
        self.result_total_label.setText(f"Total: {len(data)} item")
        return
