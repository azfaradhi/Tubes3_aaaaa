from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QPushButton
from PyQt5.QtCore import Qt

class Card(QWidget):
    def __init__(self, page_change, data, name):
        super().__init__()

        # Force size to make sure style applies
        self.setMinimumSize(200, 120)
        self.setMaximumSize(200, 200)
        self.setSizePolicy(QWidget.sizePolicy(self))

        # Wrapper frame inside the card
        wrapper = QFrame()
        wrapper.setStyleSheet("""
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 6px;
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(wrapper)

        inner_layout = QVBoxLayout(wrapper)
        inner_layout.setContentsMargins(10, 10, 10, 10)

        # Header
        title_bar = QHBoxLayout()
        title = QLabel(name)
        title.setStyleSheet("color: black;")

        title_bar.addWidget(title)
        title_bar.addStretch()

        inner_layout.addLayout(title_bar)

        # Subtitle
        subtitle = QLabel("Matched Keywords: ")
        subtitle.setStyleSheet("color: black; border: none;")
        inner_layout.addWidget(subtitle)
        inner_layout.addStretch()

        subtitle = QLabel("Contoh:")
        subtitle.setStyleSheet("color: black; border: none;")
        inner_layout.addWidget(subtitle)
        inner_layout.addStretch()

        # Footer
        footer = QHBoxLayout()

        detail_button = QPushButton("Detail")
        detail_button.setStyleSheet("""
            color: black;
            background-color: #ddd;
            border-radius: 6px;
        """)
        detail_button.setMaximumWidth(100)
        detail_button.clicked.connect(lambda: page_change(2))
        footer.addWidget(detail_button)

        cv_button = QPushButton("View CV")
        cv_button.setStyleSheet("""
            color: black;
            background-color: #ddd;
            border-radius: 6px;
        """)
        cv_button.setMaximumWidth(100)
        # cv_button.clicked.connect(lambda: page_change(2))
        footer.addWidget(cv_button)

        inner_layout.addLayout(footer)
