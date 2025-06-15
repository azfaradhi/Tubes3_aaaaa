from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt

class LandingPage(QWidget):
    def __init__(self, page_change):
        super().__init__()
        layout = QVBoxLayout(self)
        self.setStyleSheet("background-color: transparent;")  

        # Create the button column layout
        button_row = QVBoxLayout()
        button_row.setSpacing(20)

        self.analyze_button = QPushButton("CV Analyzer")
        self.analyze_button.setMinimumWidth(180)
        self.analyze_button.setMaximumWidth(200)
        self.analyze_button.setStyleSheet("""
            padding: 12px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 15px;
            background-color: #FFD700;
            color: black;
        """)
        self.analyze_button.clicked.connect(lambda: page_change(1))
        button_row.addWidget(self.analyze_button)

        self.about_button = QPushButton("About")
        self.about_button.setMinimumWidth(180)
        self.about_button.setMaximumWidth(200)
        self.about_button.setStyleSheet("""
            padding: 12px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 15px;
            background-color: #FFD700;
            color: black;
        """)
        self.about_button.clicked.connect(lambda: page_change(3))
        button_row.addWidget(self.about_button)

        # Wrap the layout in a QWidget to center it
        button_container = QWidget()
        button_container.setLayout(button_row)

        layout.addStretch()
        layout.addWidget(button_container, alignment=Qt.AlignCenter)
        layout.addStretch()
