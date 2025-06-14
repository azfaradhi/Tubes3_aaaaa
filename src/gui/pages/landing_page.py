from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QScrollArea, QPushButton,
)

class LandingPage(QWidget):

    def __init__(self, page_change):
        super().__init__()
        layout = QHBoxLayout(self)

        self.analyze_button = QPushButton("CV Analyzer")
        self.analyze_button.setMaximumWidth(200)
        self.analyze_button.setStyleSheet("padding: 10px; border-radius: 15px; background-color: #ccc;")
        self.analyze_button.clicked.connect(lambda: page_change(1))
        layout.addWidget(self.analyze_button)
